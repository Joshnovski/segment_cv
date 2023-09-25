import os
import cv2
import sys
import math
import numpy as np
import matplotlib.pyplot as plt
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from matplotlib.widgets import Cursor

from helpers import apology, login_required

# Configure application
app = Flask(__name__)

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
            flash('Image Successfully Uploaded')

            # Store filepath in user's session
            session['filepath'] = filepath

            return redirect("/dashboard")
        else: 
            return redirect("/dashboard")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("dashboard.html")
    
def load_and_preprocessing():

    # Load the image
    image = cv2.imread(session.get("filepath"))

    # Crop the bottom part of the image based on bottom_crop_ratio
    height, width, _ = image.shape
    image = image[:int(height * (1 - request.form.get("bottom-crop-ratio"))), :]

    # Convert the image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Invert the grayscale to count voids
    count_voids = request.form.get("segmentation-images")
    if count_voids:
        gray_image = cv2.bitwise_not(gray_image)

    # Equalize the histogram of the grayscale image
    equalize_hist = request.form.get("histogram-equalisation")
    if equalize_hist:
        gray_image = cv2.equalizeHist(gray_image)

    # Smooth out noise with slight blur to assist with thresholding
    kernel_size = request.form.get("blur-kernel-size")
    gray_image_blurred = cv2.GaussianBlur(gray_image, (kernel_size, kernel_size), 0)

    # Apply a threshold to the grayscale image
    grayscale_threshold_lower = request.form.get("lower-contrast-threshold")
    grayscale_threshold_upper = request.form.get("upper-contrast-threshold")

    # Set contrast limits to the grayscale image
    # _, thresholded_image = cv2.threshold(gray_image_blurred, grayscale_threshold, 255, cv2.THRESH_BINARY)
    thresholded_image = cv2.inRange(gray_image_blurred, grayscale_threshold_lower, grayscale_threshold_upper)

    # Changes the simplicity of the morphology of the segments
    grain_morphology = request.form.get("morphology-simplicity")
    thresholded_image = cv2.morphologyEx(thresholded_image, cv2.MORPH_OPEN, np.ones((grain_morphology, grain_morphology), dtype=int))

    # Convert the thresholded image to 3 channels
    thresholded_image_3chan = cv2.cvtColor(thresholded_image, cv2.COLOR_GRAY2BGR)

    # Distance transformation
    distanceTransform_threshold = request.form.get("distance-transform")
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

    # Pixel to mm converter
    scale_bar_pixels_per_mm = request.form.get("scale-to-pixel-ratio")
    pixel_size_mm = (1 / scale_bar_pixels_per_mm) ** 2

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
        grain_area = cv2.contourArea(contour)
        grain_real_area = grain_area * pixel_size_mm
        grain_area_min = request.form.get("min-size-area")
        grain_area_max = request.form.get("max-size-area")
        # histogram filtration based on selected grain range
        if grain_area_min <= grain_area < grain_area_max:
            grain_areas_filtered.append(grain_real_area)
            grain_diameters_filtered.append(area_to_diameter(grain_real_area)) # 0.680 mm
        # Sum total contoured areas and diameters
        if grain_area_min <= grain_area < grain_area_max:
            # Area total of contoured region(s)
            contour_area_total += grain_real_area
            contoured_diameter_total += area_to_diameter(grain_real_area) # mm sum
        # grain contour size range
        if grain_area_min < grain_area < grain_area_max:
            grain_contours.append(contour)
            grain_total_area += grain_area

    # Calculate average area in pixels
    grain_average_area_pixels = grain_total_area / len(grain_contours) if grain_contours else 0

    # Calculate average diameter in pixels
    grain_average_diameter_real = contoured_diameter_total / len(grain_contours) if grain_contours else 0

    # Convert average area in pixels to average area in square millimeters
    grain_average_area_mm = grain_average_area_pixels * pixel_size_mm

    # Return the number of chocolate chips, the outlined image, the thresholded image and the average area
    return contour_area_total, grain_average_diameter_real, grain_contours, grain_average_area_mm, pixel_size_mm, grain_areas, grain_diameters, grain_areas_filtered, grain_diameters_filtered

def grain_size_histogram(grain_areas_filtered, grain_diameters_filtered):

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
    # Calculate bin_width
    n = request.form.get("histogram-bins")
    # Plot first histogram
    ax1.hist(grain_areas_filtered, bins=n, color='orange', alpha=1, range=(min(grain_areas_filtered), max(grain_areas_filtered)), edgecolor='white', label='Areas Selected (Excluding Uncertain Contours)')
    ax1.set_xlabel('Grain Area (mm\u00b2)')
    ax1.set_ylabel('Count of Grains')
    ax1.set_title(f'Contoured Area Histogram')

    # Plot the second histogram
    ax2.hist(grain_diameters_filtered, bins=n, color='orange', alpha=1, range=(min(grain_diameters_filtered), max(grain_diameters_filtered)), edgecolor='white', label='Diameters Selected (Excluding Uncertain Contours)')
    ax2.set_xlabel('Grain Diameters (\u03BCm)')
    ax2.set_ylabel('Count of Grains')
    ax2.set_title(f'Contoured Diameter Histogram')

    # legend positioning
    ax1.legend(loc="upper right")
    ax2.legend(loc="upper right")

    # Adds labels to bars in the bar container
    for grains in ax1.containers:
        ax1.bar_label(grains)
    for grains in ax2.containers:
        ax2.bar_label(grains)

    # adjust subplot parameters so subplots are fit well in the figure
    plt.tight_layout()
    plt.show(block=False)

def draw_contours(image, grain_contours):

    # Copy the original image to edit
    result_image = image.copy()

    # Inverted grayscale image
    # result_image = cv2.bitwise_not(result_image)

    # Draws contour lines over the copied image
    cv2.drawContours(result_image, grain_contours, -1, (255, 0, 0), request.form.get("contour-thickness"))

    return result_image

def display_images(watershed_imaged, outlined_image_cv, distance_transform_thresholded, original_image, thresholded_image_3chan, distance_transform):

    fig, ((ax1, ax2, ax3), (ax4, ax5, ax6)) = plt.subplots(2, 3, figsize=(12, 8), sharex='all', sharey='all')

    ax5.imshow(watershed_imaged, cmap='gray')
    ax5.set_title(f'Watershed Segmented')
    ax5.axis('off')
    Cursor(ax5, useblit=True, color='red', linewidth=1)
    plt.savefig('static/images/watershed_image.png')

    ax6.imshow(cv2.cvtColor(outlined_image_cv, cv2.COLOR_BGR2RGB))
    ax6.set_title(f'Contour Outlines')
    ax6.axis('off')
    Cursor(ax6, useblit=True, color='red', linewidth=1)
    plt.savefig('static/images/contoured_image.png')

    ax4.imshow(cv2.cvtColor(distance_transform_thresholded, cv2.COLOR_BGR2RGB))
    ax4.set_title(f'Binary Distance Transform')
    ax4.axis('off')
    Cursor(ax4, useblit=True, color='red', linewidth=1)
    plt.savefig('static/images/dtt.png')

    ax1.imshow(cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB))
    ax1.set_title(f'Original Image')
    ax1.axis('off')
    Cursor(ax1, useblit=True, color='red', linewidth=1)
    plt.savefig('static/images/original_image.png')

    ax2.imshow(cv2.cvtColor(thresholded_image_3chan, cv2.COLOR_BGR2RGB))
    ax2.set_title(f'Binary Thresholded Contrast')
    ax2.axis('off')
    Cursor(ax2, useblit=True, color='red', linewidth=1)
    plt.savefig('static/images/thresholded_image_3chan.png')

    ax3.imshow(cv2.cvtColor(distance_transform, cv2.COLOR_BGR2RGB))
    ax3.set_title(f'Distance Transform')
    ax3.axis('off')
    Cursor(ax3, useblit=True, color='red', linewidth=1)
    plt.savefig('static/images/dt.png')

    plt.tight_layout()
    plt.show()

@app.route("/run", methods=['POST'])    
def run():
    # Run through all the functions
    thresholded_image_3chan, markers, image, dtt, dt = load_and_preprocessing()
    watershed_image = watershed_and_postprocessing(thresholded_image_3chan, markers)
    contour_area_total, grain_average_diameter_real, grain_contours, grain_average_area_mm, pixel_size_mm, grain_areas, grain_diameters, grain_areas_filtered, grain_diameters_filtered = calculate_area_and_filter_contours(watershed_image)
    contoured_image = draw_contours(image, grain_contours)

    if request.form.get("show-size-histogram"):
        grain_size_histogram(grain_areas_filtered, grain_diameters_filtered)

    if request.form.get("segmentation-images"):
        display_images(watershed_image, contoured_image, dtt, image, thresholded_image_3chan, dt)
    return redirect("/dashboard") 