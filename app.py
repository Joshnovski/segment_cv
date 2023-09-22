import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///segment.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
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
        return redirect("/dashboard")

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

        return redirect("/dashboard")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")
    
@app.route("/dashboard")
def dashboard():
    """User accesses dashboard after logging in"""

    # Ensure user is logged in else redirect to login page
    if not session.get("user_id"):
        return redirect("/")

    # Redirect user to home page
    return render_template("dashboard.html")
