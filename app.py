import os
import cv2
import math
import time
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import logging as lg # REMOVE THIS LINE LATER!
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, jsonify, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from matplotlib.widgets import Cursor
from helpers import apology, login_required
 
# Configure application here
app = Flask(__name__)

# Set logging level
lg.getLogger('matplotlib').setLevel(lg.ERROR)
lg.getLogger('PIL').setLevel(lg.ERROR)

# Change to Agg backend for matplotlib
matplotlib.use('Agg')

# Set tje upload folder configuration
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder  exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///segment.db")

# Cleanup sessions older than 1 day
session_dir = 'flask_session'
session_lifetime = 1 * 1 * 60 * 60 # 1 hour
now = time.time()
for filename in os.listdir(session_dir):
    file_path = os.path.join(session_dir, filename)
    if os.path.getmtime(file_path) < now - session_lifetime:
        os.remove(file_path)

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

        # Ensure both username and password were submitted
        if not username and not password:
            flash('Must provide username and password', 'error')
            return render_template("login.html")

        # Ensure username was submitted
        elif not username:
            flash('Must provide a username', 'error')
            return render_template("login.html")

        # Ensure password was submitted
        elif not password:
            flash('Must provide password', 'error')
            return render_template("login.html")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], password):
            flash('Invalid username and/or password', 'error')
            return render_template("login.html")

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

        # Ensure username and both password fields are filled
        if username == "" or password == "" or confirmation == "":
            flash('Some fields have been left blank', 'error')
            return render_template("register.html")

        # Ensure username exists
        elif len(rows) == 1:
            flash('Username already exists', 'error')
            return render_template("register.html")
        
        # Ensure username has between 3 and 12 characters
        elif len(username) < 3 or len(username) > 12:
            flash("Username must be between 3 and 12 characters", 'error')
            return render_template("register.html")

        # Ensure password is sufficiently secure
        if len(password) < 8:
            flash("Password must be at least 8 characters, and contain at least one number, uppercase letter, lowercase letter and symbol", 'error')
            return render_template("register.html")
        elif not any(char.isdigit() for char in password):
            flash("Password must be at least 8 characters, and contain at least one number, uppercase letter, lowercase letter and symbol", 'error')
            return render_template("register.html")
        elif not any(char.isupper() for char in password):
            flash("Password must be at least 8 characters, and contain at least one number, uppercase letter, lowercase letter and symbol", 'error')
            return render_template("register.html")
        elif not any(char.islower() for char in password):
            flash("Password must be at least 8 characters, and contain at least one number, uppercase letter, lowercase letter and symbol", 'error')
            return render_template("register.html")
        elif not any(not char.isalnum() for char in password):
            flash("Password must be at least 8 characters, and contain at least one number, uppercase letter, lowercase letter and symbol", 'error')
            return render_template("register.html")
        


        # Ensure password was submitted
        elif not password == confirmation:
            flash("Password and confirmation do not match", 'error')
            return render_template("register.html")

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
    
    # Retrieve from the session after run, else set to None
    area_histogram_div = session.get('area_histogram_div', None)
    diameter_histogram_div = session.get('diameter_histogram_div', None)

    user = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])

    # Redirect user to home page
    return render_template("dashboard.html", username=user[0]['username'], os=os, images_existing=len(os.listdir('static/images')), area_histogram_div=area_histogram_div, diameter_histogram_div=diameter_histogram_div)

##############################################################################################################################################

@app.route("/upload", methods=["POST"])
def upload_image():
    """User is prompted to select an image after clicking image icon. Image is then stored as a variable"""

    # Ensure user is logged in else redirect to login page
    if not session.get("user_id"):
        return redirect("/")

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            flash('Image Successfully Uploaded', 'success')

            # Store filepath in user's session
            session['filepath'] = filepath

            return redirect("/dashboard")
        else:
            flash('Please Upload Image', 'error') 
            return redirect("/dashboard")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("dashboard.html")

@app.before_request
def set_initial_parameters():

    """ Initialise the parameters in the session. Might be possible to scale this for multiple pre-sets. """

    # If the session is starting for the first time, clear the processed images and uploaded images.
    if not session.get('initialized'):
        try:
            for file in os.listdir('static/images'):
                    os.remove(f'static/images/{file}')
            for file in os.listdir('static/uploads'):
                os.remove(f'static/uploads/{file}')
        except (PermissionError, FileNotFoundError):
            pass
        session['initialized'] = True

    # If the session is starting for the first time, set the parameters and results to default values
    if not session.get('parameters_set'):

        # Scale calculator
        session['pixel-distance'] = 2559.8
        session['scalebar-length'] = 10
        session['scale-to-pixel-ratio'] = round(session['pixel-distance'] / session['scalebar-length'], 2)

        # Control Center Parameters
        session['bottom-crop-ratio'] = 0.05
        session['show-size-histogram'] = "on"
        session['segmentation-images'] = "on"
        session['histogram-bins'] = 20
        session['contour-thickness'] = 10
        session['invert-grayscale'] = None
        session['histogram-equalisation'] = "on"
        session['lower-contrast-threshold'] = 170
        session['upper-contrast-threshold'] = 255
        session['blur-kernel-size'] = 3
        session['distance-transform'] = 7
        session['morphology-simplicity'] = 3
        session['min-size-diameter'] = 0.283
        session['max-size-diameter'] = 1.373

        # Locks out the repeated setting of parameters if they have already been set.
        session['parameters_set'] = True

@app.route("/calculate-scale", methods=["POST"])
def calculate_scale():

    # Calculate the scale value if the user changed input
    session['pixel-distance'] = float(request.form.get("pixel-distance"))
    session['scalebar-length'] = float(request.form.get("scalebar-length"))

    session['scale-to-pixel-ratio'] = round(session['pixel-distance'] / session['scalebar-length'], 2)

    flash('Calculation Complete! Control Center Updated', 'success')

    return redirect("/dashboard") 

@app.route("/reset", methods=["POST"])
def reset_parameters():

    # Reset parameters without also removing the already uploaded image
    session['initialized'] = True
    # Reset session check for parameters to pass if statement in set_initial_parameters()
    session.pop('parameters_set', None)
    # Run the set initial parameters function to reset the parameters
    set_initial_parameters()
    return redirect("/dashboard")

@app.route("/store-parameters", methods=["POST"])
def store_parameters():
    """ Only triggers once a change in the input has been detected but doesn't store values to session otherwise.
    Works in conjunction with set_initial_parameters() to store the values in the session. """

    # Dictionary of parameters, their expected types, and validation functions
    params = {
        # 'bottom-crop-ratio': (float, None),
        'show-size-histogram': (str, None),
        'segmentation-images': (str, None),
        'histogram-bins': (int, lambda x: x >= 0 and x <= 100),
        'contour-thickness': (int, lambda x: x > 0 and x <= 100),
        'invert-grayscale': (str, None),
        'histogram-equalisation': (str, None),
        'lower-contrast-threshold': (int, lambda x: x >= 0 and x <= 255),
        'upper-contrast-threshold': (int, lambda x: x >= 0 and x <= 255),
        'blur-kernel-size': (int, lambda x: x > 0 and x % 2 == 1),
        'distance-transform': (int, lambda x: x >= 0 and x <= 255),
        'morphology-simplicity': (int, lambda x: x >= 0 and x <= 500),
        'min-size-diameter': (float, lambda x: x >= 0 and x <= 1000),
        'max-size-diameter': (float, lambda x: x >= 0 and x <= 1000),
    }

    # Error messages for specific validations
    error_messages = {
        'blur-kernel-size': 'Blur Kernel Size must be odd and positive',
    }

    error_response = []

    for param, (data_type, validator) in params.items():
        try:
            raw_value = request.form.get(param)

            # Special handling for checkboxes
            if param in ["invert-grayscale", "histogram-equalisation"]:
                session[param] = "on" if raw_value else None
                continue

            # Check if raw_value is None before casting
            if raw_value is None:
                error_response.append(f"Missing value for {param}")
                continue

            value = data_type(raw_value)

            if validator and not validator(value):
                error_response.append(error_messages.get(param, f"Invalid value for {param}"))
                continue

            session[param] = value

        except ValueError as e:
            error_response.append(str(e))

    else:
        return jsonify(success=True)


def load_and_preprocessing():

    # Load the image
    image = cv2.imread(session.get("filepath"))

    # Crop the bottom part of the image based on bottom_crop_ratio
    height, width, _ = image.shape
    image = image[:int(height * (1 - session.get("bottom-crop-ratio"))), :]

    # Convert the image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Invert the grayscale to count voids
    count_voids = session.get("invert-grayscale")
    if count_voids:
        gray_image = cv2.bitwise_not(gray_image)

    # Equalize the histogram of the grayscale image
    equalize_hist = session.get("histogram-equalisation")
    if equalize_hist:
        gray_image = cv2.equalizeHist(gray_image)

    # Smooth out noise with slight blur to assist with thresholding
    kernel_size = session.get("blur-kernel-size")
    gray_image_blurred = cv2.GaussianBlur(gray_image, (kernel_size, kernel_size), 0)

    # Apply a threshold to the grayscale image
    grayscale_threshold_lower = session.get("lower-contrast-threshold")
    grayscale_threshold_upper = session.get("upper-contrast-threshold")

    # Set contrast limits to the grayscale image
    # _, thresholded_image = cv2.threshold(gray_image_blurred, grayscale_threshold, 255, cv2.THRESH_BINARY)
    thresholded_image = cv2.inRange(gray_image_blurred, grayscale_threshold_lower, grayscale_threshold_upper)

    # Changes the simplicity of the morphology of the segments
    grain_morphology = session.get("morphology-simplicity")
    thresholded_image = cv2.morphologyEx(thresholded_image, cv2.MORPH_OPEN, np.ones((grain_morphology, grain_morphology), dtype=int))

    # Convert the thresholded image to 3 channels
    thresholded_image_3chan = cv2.cvtColor(thresholded_image, cv2.COLOR_GRAY2BGR)

    # Distance transformation
    distanceTransform_threshold = session.get("distance-transform")
    dt = cv2.distanceTransform(thresholded_image, cv2.DIST_L2, 3)
    dt = ((dt - dt.min()) / (dt.max() - dt.min()) * 255).astype(np.uint8)
    _, dtt = cv2.threshold(dt, distanceTransform_threshold, 255, cv2.THRESH_BINARY)

    border = cv2.dilate(thresholded_image, None, iterations=5)
    border = border - cv2.erode(border, None)

    dtt = dtt.astype(np.uint8)
    _, markers = cv2.connectedComponents(dtt)

    # Completing the markers now.
    markers[border == 255] = 255
    markers = markers.astype(np.int32)

    return thresholded_image_3chan, markers, image, dtt, dt

def watershed_and_postprocessing(thresholded_image_3chan, markers):
    # The watershed algorithm modifies the markers image
    cv2.watershed(thresholded_image_3chan, markers)
    # image[markers == -1] = [0, 0, 255]

    # Create a binary image that marks the borders (where markers == -1)
    border_mask = np.where(markers == -1, 255, 0).astype(np.uint8)

    # Border Thickness
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    dilated_border_mask = cv2.dilate(border_mask, kernel, iterations=2)

    # Create a grayscale image where the separated grains have their marker values
    # (with the labels gradient) and everything else is white
    separated_grains_image = np.where(markers > 1, markers, 255).astype(np.uint8)

    # Normalize the separated_grains_image to have a full range of grayscale values
    separated_grains_image = cv2.normalize(separated_grains_image, None, 0, 255, cv2.NORM_MINMAX)

    # Apply the mask to the result image
    result = np.where(dilated_border_mask == 255, dilated_border_mask, separated_grains_image)
    result = 255 - result
    _, result = cv2.threshold(result, 0, 255, cv2.THRESH_BINARY)

    return result

def area_to_diameter(area):
    return math.sqrt(4*float(area)/math.pi)

def diameter_to_area(diameter):
    return math.pi*(float(diameter)/2)**2

def calculate_area_and_filter_contours(result):
    # Find contours in the new blurred_image
    contours, _ = cv2.findContours(result, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Pixel to real units converter
    scale_bar_pixels_per_unit = session.get("scale-to-pixel-ratio")
    # (units/pixel)^2
    pixel_size_real = (1 / scale_bar_pixels_per_unit) ** 2

    # Initialise contour groups arrays
    grain_contours = []
    # Initialise all areas and filtered areas arrays
    grain_areas = []
    grain_areas_filtered = []
    # Initialise all diameters and filtered diameters arrays
    grain_diameters = []
    grain_diameters_filtered = []

    # Initialise contour surface area total between selected size range
    contour_area_total = 0
    #  Initialise contour group surface area total ( used to get average grain area based on # of contours )
    grain_total_area = 0
    # Initialise total sum of diameters
    contoured_diameter_total = 0

    # Filter contours based on size and shape - first pass
    for contour in contours:
        # Calculates the area in pixels^2 for each contoured segment
        grain_area = cv2.contourArea(contour)
        # Convert the area in pixels^2 to real units^2
        grain_real_area = grain_area * pixel_size_real
        # Calculate filtration boundaries by units/(units/pixel)^2 = pixels^2/units
        grain_area_min = diameter_to_area(session.get("min-size-diameter"))
        grain_area_max = diameter_to_area(session.get("max-size-diameter"))
        # histogram filtration based on selected grain range
        if grain_area_min <= grain_real_area < grain_area_max:
            grain_areas_filtered.append(grain_real_area)
            grain_diameters_filtered.append(area_to_diameter(grain_real_area))
        # Sum total contoured areas and diameters
        if grain_area_min <= grain_real_area < grain_area_max:
            # Area total of contoured region(s)
            contour_area_total += grain_real_area
            contoured_diameter_total += area_to_diameter(grain_real_area)
        # grain contour size range
        if grain_area_min < grain_real_area < grain_area_max:
            grain_contours.append(contour)
            grain_total_area += grain_real_area

    # Calculate average area in real units^2
    grain_average_area = grain_total_area / len(grain_contours) if grain_contours else 0

    # Calculate average diameter in real units
    grain_average_diameter = contoured_diameter_total / len(grain_contours) if grain_contours else 0

    # Store the average grain diameter in the session
    session['average-grain-diameter'] = round(grain_average_diameter, 2)
    # Store the average grain area in the session
    session['average-grain-area'] = round(grain_average_area, 2)
    # Store the number of segments in the session
    session['number-of-segments'] = len(grain_contours)

    # Return the number of chocolate chips, the outlined image, the thresholded image and the average area
    return contour_area_total, grain_average_diameter, grain_contours, grain_average_area, pixel_size_real, grain_areas, grain_diameters, grain_areas_filtered, grain_diameters_filtered

def grain_size_histogram(grain_areas_filtered, grain_diameters_filtered):

    # style histograms
    n = session['histogram-bins']
    def plot_histogram(data, label, file_name):
        if not data:
            min_range, max_range = 0, 0
        else:
            min_range, max_range = min(data), max(data)
        fig, ax = plt.subplots(figsize=(14, 6))
        ax.hist(data, bins=n, color='#1d897b', alpha=1, range=(min_range, max_range), edgecolor='#262626')
        # Label and title styles
        ax.set_xlabel(label, color='white', fontsize = 14)
        ax.set_ylabel('Count of Segments', color='white', fontsize = 14)
        # Tick colors
        ax.tick_params(axis='both', colors='white')
        # Grid color
        ax.yaxis.grid(True, linestyle='--', which='major', color='#575757', alpha=.25)
        # Set background colors
        ax.set_facecolor('#262626') # for the main background
        fig.set_facecolor('#262626') # for space around the plot
        ax.spines['bottom'].set_color('white')
        ax.spines['top'].set_color('#262626')
        ax.spines['right'].set_color('#262626')
        ax.spines['left'].set_color('#262626')

        plt.savefig(file_name, bbox_inches='tight', pad_inches=0, facecolor=fig.get_facecolor())
        plt.close(fig)

    plot_histogram(grain_areas_filtered, 'Area (mm\u00b2)', 'static/images/area_histogram.png')
    plot_histogram(grain_diameters_filtered, 'Diameter (\u03BCm)', 'static/images/diameter_histogram.png')

def draw_contours(image, grain_contours):

    # Copy the original image to edit
    result_image = image.copy()

    # Inverted grayscale image
    # result_image = cv2.bitwise_not(result_image)

    # Draws contour lines over the copied image
    cv2.drawContours(result_image, grain_contours, -1, (123, 137, 29), session.get("contour-thickness"))

    return result_image

def display_images(watershed_image, contoured_image, distance_transform_thresholded, original_image, thresholded_image_3chan, distance_transform):

    # Store each image in a list
    images = [
        (watershed_image, "watershed_image"), 
        (contoured_image, "contoured_image"), 
        (distance_transform_thresholded, "distance_transform_thresholded"), 
        (original_image, "original_image"), 
        (thresholded_image_3chan, "thresholded_image_3chan"), 
        (distance_transform, "distance_transform")]
    
    # Create each figure and save it.
    for image, filename in images:
        # Create new figure
        #Get image size
        fig, ax = plt.subplots(figsize=(6, 6))
        # Check if the image is grayscale or RGB
        if len(image.shape) == 2 or image.shape[2] == 1:
            # Grayscale image
            cmap = 'gray'
        else:
            # RGB image
            cmap = None
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # Display the image
        ax.imshow(image, cmap=cmap)
        ax.axis('off')
        # Save the figure
        plt.savefig(f'static/images/{filename}.png', bbox_inches='tight', pad_inches=0)
        # Close the figure
        plt.close(fig)

@app.route("/run", methods=['POST'])    
def run():

    if cv2.imread(session.get("filepath")) is None:
        flash('Please Upload Image', 'error') 
        return redirect("/dashboard")

    # Run through all the functions
    thresholded_image_3chan, markers, image, dtt, dt = load_and_preprocessing()
    watershed_image = watershed_and_postprocessing(thresholded_image_3chan, markers)
    _, _, grain_contours, _, _, _, _, grain_areas_filtered, grain_diameters_filtered = calculate_area_and_filter_contours(watershed_image)
    contoured_image = draw_contours(image, grain_contours)
    grain_size_histogram(grain_areas_filtered, grain_diameters_filtered)
    display_images(watershed_image, contoured_image, dtt, image, thresholded_image_3chan, dt)

    # Flash a success message
    flash('Segmentation Complete', 'success')

    return redirect("/dashboard") 