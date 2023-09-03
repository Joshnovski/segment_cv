import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    # Gather purchase history information
    symbol = db.execute(
        "SELECT symbol FROM purchases WHERE user_id = ?", session["user_id"]
    )
    shares = db.execute(
        "SELECT shares FROM purchases WHERE user_id = ?", session["user_id"]
    )
    price = db.execute(
        "SELECT price FROM purchases WHERE user_id = ?", session["user_id"]
    )
    print(symbol)

    # Total Spent
    total_spent = 0
    for i in range(len(symbol)):
        total_spent += price[i]["price"] * shares[i]["shares"]

    # Wallet funds remaining of user that has logged in
    user_cash_dict = db.execute(
        "SELECT cash FROM users WHERE id = ?", session["user_id"]
    )
    user_cash = user_cash_dict[0]["cash"]

    return render_template(
        "index.html",
        symbol=symbol,
        shares=shares,
        price=price,
        total_spent="{:.2f}".format(total_spent),
        user_cash="{:.2f}".format(user_cash),
    )


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    if request.method == "POST":
        # Store symbol value for later database querying
        symbol = request.form.get("symbol").upper()

        # loopup company stock price and name via symbol
        searched_quote_dict = lookup(symbol)

        # Return apology if no symbol added or doesn't exist
        if symbol == "" or searched_quote_dict == None:
            return apology("Invalid Symbol", 400)

        # Get valid shares amount from user input
        try:
            shares = int(request.form.get("shares"))
            if not shares > 0:
                return apology("Must be a positive integer", 400)
        except ValueError:
            return apology("Invalid share value", 400)

        # Process the purchase #

        # Collect share price info
        price = searched_quote_dict["price"]

        # get cash of user that has logged in
        user_cash_dict = db.execute(
            "SELECT cash FROM users WHERE id = ?", session["user_id"]
        )
        user_cash = user_cash_dict[0]["cash"]

        # Check if enough funds for purchase
        if user_cash < price * shares:
            return apology("Insufficent funds", 400)

        # If extra share bought later, add to current shares #

        check_shares = db.execute(
            "SELECT shares FROM purchases WHERE symbol = ? AND user_id = ?",
            symbol,
            session["user_id"],
        )

        # Store each buy into purchase history
        db.execute(
            "INSERT INTO purchases_history (user_id, symbol, shares, price) VALUES (?, ?, ?, ?)",
            session["user_id"],
            symbol,
            shares,
            price,
        )

        if check_shares == []:
            # Insert into the purchases table
            db.execute(
                "INSERT INTO purchases (user_id, symbol, shares, price) VALUES (?, ?, ?, ?)",
                session["user_id"],
                symbol,
                shares,
                price,
            )
        else:
            # Update share values
            updated_shares = check_shares[0]["shares"] + shares

            # Update owned shares
            db.execute(
                "UPDATE purchases SET shares = ? WHERE symbol = ? AND user_id = ?",
                updated_shares,
                symbol,
                session["user_id"],
            )

        # Update the user's cash
        user_cash_update = user_cash - (price * shares)
        db.execute(
            "UPDATE users SET cash = ? WHERE id = ?",
            user_cash_update,
            session["user_id"],
        )

        # Redirect user to home page
        return redirect("/")
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    # Gather purchase/sell history information #

    symbol = db.execute(
        "SELECT symbol FROM purchases_history WHERE user_id = ?", session["user_id"]
    )
    shares = db.execute(
        "SELECT shares FROM purchases_history WHERE user_id = ?", session["user_id"]
    )
    price = db.execute(
        "SELECT price FROM purchases_history WHERE user_id = ?", session["user_id"]
    )
    timestamp = db.execute(
        "SELECT timestamp FROM purchases_history WHERE user_id = ?", session["user_id"]
    )

    return render_template(
        "history.html", symbol=symbol, shares=shares, price=price, timestamp=timestamp
    )


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Retrieve username and password from form
        username = request.form.get("username")
        password = request.form.get("password")

        # Ensure username was submitted
        if not username:
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not password:
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], password):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in (ensures logged in UI)
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required  # Defined in helpers.py
def quote():
    """Get stock quote."""

    # look up stock's current price whos text field name is symbol
    # allow input of stock symbol as text field
    if request.method == "POST":
        # Store symbol value for later database querying
        symbol = request.form.get("symbol").upper()

        # Redirect back to page if no symbol added
        if symbol == "":
            return apology("Invalid Symbol", 400)

        # loopup company stock price and name via symbol
        searched_quote_dict = lookup(symbol)
        # NoneType
        if searched_quote_dict == None:
            return apology("Invalid Symbol", 400)

        name = searched_quote_dict["name"]
        price = usd(searched_quote_dict["price"])

        # Render the quoted page, returning name, price and symbol
        return render_template("quoted.html", name=name, price=price, symbol=symbol)
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # Forget any user_id info
    session.clear()

    # require a username (as text whose name is username)... Render apology if input is blank or already exists

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Retrieve username and password from textbox
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # require a password and a confirmation of the same password... render apology if blank or not match

        # Query database for existing username
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        # Ensure username exists
        if len(rows) == 1:
            return apology("Username already exists", 400)

        # Ensure username field left blank
        elif username == "":
            return apology("Username is required", 400)

        # Ensure both password fields are filled
        elif password == "" or confirmation == "":
            return apology("Password and confirmation is required", 400)

        # Ensure password was submitted
        elif not password == confirmation:
            return apology("Password confirmation doesn't match", 400)

        # Makes a hash code of the password
        hashed_password = generate_password_hash(password)

        # INSERT new user into 'users', storing the username and a hash of the password.
        db.execute(
            "INSERT INTO users (username, hash) VALUES (?, ?)",
            username,
            hashed_password,
        )

        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    # Get stock symbols from purchased list
    purchased_stock_symbols = db.execute(
        "SELECT symbol FROM purchases WHERE user_id = ?", session["user_id"]
    )

    if request.method == "POST":
        # Record user selection of owned stock symbol
        try:
            symbol_selection = request.form.get("symbol")
            if symbol_selection == None:
                return apology("Invalid symbol", 400)
        except ValueError:
            return apology("Invalid symbol", 400)

        # Note the amount of shares owned for the selected stock symbol
        owned_shares = db.execute(
            "SELECT shares FROM purchases WHERE symbol = ?", symbol_selection
        )

        # Get valid shares amount from user input
        try:
            shares = int(request.form.get("shares"))
            if not shares > 0:
                return apology("Must be a positive integer", 400)
            elif owned_shares[0]["shares"] < shares:
                return apology("Selling more shares than owned", 400)
        except ValueError:
            return apology("Invalid share value", 400)

        # Selling component #

        # Get value of share(s) being sold
        purchased_share_value_dict = db.execute(
            "SELECT price FROM purchases WHERE symbol = ? AND user_id = ?",
            symbol_selection,
            session["user_id"],
        )
        total_share_value = purchased_share_value_dict[0]["price"] * shares

        # get cash of user that has logged in
        user_cash_dict = db.execute(
            "SELECT cash FROM users WHERE id = ?", session["user_id"]
        )
        user_cash = user_cash_dict[0]["cash"]

        # Add sold shares to users wallet value
        updated_user_cash = user_cash + total_share_value

        # Add value of sold shares back to wallet
        db.execute(
            "UPDATE users SET cash = ? WHERE id = ?",
            updated_user_cash,
            session["user_id"],
        )

        # Update the owned shares information #
        updated_share_count = owned_shares[0]["shares"] - shares

        if updated_share_count == 0:
            # remove row from purchases
            db.execute(
                "DELETE FROM purchases WHERE symbol = ? AND user_id = ?",
                symbol_selection,
                session["user_id"],
            )
        elif updated_share_count > 0:
            # Update 'shares' column to new value
            db.execute(
                "UPDATE purchases SET shares = ? WHERE user_id = ? AND symbol = ?",
                updated_share_count,
                session["user_id"],
                symbol_selection,
            )

        # Store each sell into purchase history
        sell_share = -shares
        share_price = purchased_share_value_dict[0]["price"]
        db.execute(
            "INSERT INTO purchases_history (user_id, symbol, shares, price) VALUES (?, ?, ?, ?)",
            session["user_id"],
            symbol_selection,
            sell_share,
            share_price,
        )

        # Redirect user to home page
        return redirect("/")
    else:
        return render_template(
            "sell.html", purchased_stock_symbols=purchased_stock_symbols
        )


@app.route("/wallet", methods=["GET", "POST"])
@login_required  # Defined in helpers.py
def wallet():
    """Add money to wallet."""

    # look up stock's current price whos text field name is symbol
    # allow input of stock symbol as text field
    if request.method == "POST":
        # Get user input funds
        try:
            add_funds = float(request.form.get("add_funds"))
            if not add_funds > 0:
                return apology("Must be a positive integer", 400)
        except ValueError:
            return apology("Invalid funds value", 400)

        # Get wallet value
        wallet_value_dict = db.execute(
            "SELECT cash FROM users WHERE id = ?", session["user_id"]
        )
        wallet_value = wallet_value_dict[0]["cash"]

        # Add funds to current wallet value
        new_wallet_value = wallet_value + add_funds

        # Update funds to account
        db.execute(
            "UPDATE users SET cash = ? WHERE id = ?",
            new_wallet_value,
            session["user_id"],
        )

        return redirect("/")
    else:
        # Get wallet value
        wallet_value_dict = db.execute(
            "SELECT cash FROM users WHERE id = ?", session["user_id"]
        )
        wallet_value = wallet_value_dict[0]["cash"]

        return render_template("wallet.html", wallet_value=wallet_value)
