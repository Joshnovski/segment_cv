import cv2
import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Cursor
import config_watershedAll
from tkinter import filedialog

# Click dectection initialisation
click_location = None


def on_press(event):
    global click_location
    click_location = (event.x, event.y)


def on_release(event):
    global click_location
    if event.inaxes is None:
        return
    # Determine if the moise moved significantly
    dx = abs(event.x - click_location[0])
    dy = abs(event.y - click_location[1])

    # If a click and not a drag
    if dx < 5 and dy < 5 and event.inaxes:
        fig, ax = plt.subplots(1,1, figsize=(8, 8))
        ax.imshow(event.inaxes.images[0].get_array(), cmap='gray')
        ax.set_title(event.inaxes.get_title())
        ax.axis('off')
        Cursor(ax, useblit=True, color='red', linewidth=1)
        plt.show()


def init_GUI_variables():

    global scale_factor
    global scale_bar_pixels_per_mm
    global bottom_crop_ratio

    global show_hist
    global show_images
    global histogram_bins
    global contour_thickness

    global count_voids
    global equalize_hist
    global grayscale_threshold_lower
    global grayscale_threshold_upper
    global kernel_size
    global distanceTransform_threshold
    global grain_morphology

    global grain_area_min
    global grain_area_max

    global grain_diameter_min
    global grain_diameter_max

    global pixel_size_mm

    scale_factor = config_watershedAll.scale_factor.get()
    scale_bar_pixels_per_mm = config_watershedAll.scale_bar_pixels_per_mm.get()
    bottom_crop_ratio = config_watershedAll.bottom_crop_ratio.get()

    show_hist = config_watershedAll.show_hist.get()
    show_images = config_watershedAll.show_images.get()
    histogram_bins = config_watershedAll.histogram_bins.get()
    contour_thickness = config_watershedAll.contour_thickness.get()

    count_voids = config_watershedAll.count_voids.get()
    equalize_hist = config_watershedAll.equalize_hist.get()
    grayscale_threshold_lower = config_watershedAll.grayscale_threshold_lower.get()
    grayscale_threshold_upper = config_watershedAll.grayscale_threshold_upper.get()
    kernel_size = config_watershedAll.kernel_size.get()
    distanceTransform_threshold = config_watershedAll.distanceTransform_threshold.get()
    grain_morphology = config_watershedAll.grain_morphology.get()

    pixel_size_mm = (1 / scale_bar_pixels_per_mm) ** 2

    grain_area_min = (config_watershedAll.grain_area_min.get()) / pixel_size_mm
    grain_area_max = (config_watershedAll.grain_area_max.get()) / pixel_size_mm

    grain_diameter_min = (config_watershedAll.grain_diameter_min.get())
    grain_diameter_max = (config_watershedAll.grain_diameter_max.get())

    return


def select_file():
    global image_path

    # opens fileselector and prioritised .tiff formats but can use any image.
    image_path = filedialog.askopenfilename(initialdir="/", title="Select file",
                                            filetypes=(("tiff files", "*.tiff"), ("all files", "*.*")))
    # Ensure file as been chosen;
    if not image_path:
        print("No file selected!")
        return


def count_type():
    if count_voids:
        grain_or_void = "void"
    else:
        grain_or_void = "grain"

    return grain_or_void


def load_and_preprocessing():
    # Load the image
    image = cv2.imread(image_path)

    # error capture
    if image is None:
        print(f"Error: Unable to load image from {image_path}")
        sys.exit()

    # Crop the bottom part of the image based on bottom_crop_ratio
    height, width, _ = image.shape
    image = image[:int(height * (1 - bottom_crop_ratio)), :]

    # Resize the image if scale_factor is not 1
    if scale_factor != 1:
        image = cv2.resize(image, (int(image.shape[1] * scale_factor), int(image.shape[0] * scale_factor)))

    # Convert the image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Invert the grayscale to count voids
    if count_voids:
        gray_image = cv2.bitwise_not(gray_image)

    # Equalize the histogram of the grayscale image
    if equalize_hist:
        gray_image = cv2.equalizeHist(gray_image)

    # Smooth out noise with slight blur to assist with thresholding
    gray_image_blurred = cv2.GaussianBlur(gray_image, (kernel_size, kernel_size), 0)

    # Apply a threshold to the grayscale image
    # _, thresholded_image = cv2.threshold(gray_image_blurred, grayscale_threshold, 255, cv2.THRESH_BINARY)
    thresholded_image = cv2.inRange(gray_image_blurred, grayscale_threshold_lower, grayscale_threshold_upper)

    thresholded_image = cv2.morphologyEx(thresholded_image, cv2.MORPH_OPEN, np.ones((grain_morphology, grain_morphology), dtype=int))

    thresholded_image_3chan = cv2.cvtColor(thresholded_image, cv2.COLOR_GRAY2BGR)

    # Distance transformation
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


def calculate_area_and_filter_contours(result):

    # Find contours in the new blurred_image
    contours, _ = cv2.findContours(result, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Pixel to mm converter
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
        # histogram filtration based on selected grain range
        if grain_area_min <= grain_area < grain_area_max:
            grain_areas_filtered.append(grain_real_area)
            grain_diameters_filtered.append(config_watershedAll.area_to_diameter(grain_real_area)) # 0.680 mm
        # Sum total contoured areas and diameters
        if grain_area_min <= grain_area < grain_area_max:
            # Area total of contoured region(s)
            contour_area_total += grain_real_area
            contoured_diameter_total += config_watershedAll.area_to_diameter(grain_real_area) # mm sum
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

    # Note if grain or void counting
    grain_or_void = count_type()
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
    # Calculate bin_width
    n = histogram_bins
    # Plot first histogram
    ax1.hist(grain_areas_filtered, bins=n, color='orange', alpha=1, range=(min(grain_areas_filtered), max(grain_areas_filtered)), edgecolor='white', label='Areas Selected (Excluding Uncertain Contours)')
    ax1.set_xlabel('Grain Area (mm\u00b2)')
    ax1.set_ylabel('Count of Grains')
    ax1.set_title(f'{grain_or_void} area histogram')

    # Plot the second histogram
    ax2.hist(grain_diameters_filtered, bins=n, color='orange', alpha=1, range=(min(grain_diameters_filtered), max(grain_diameters_filtered)), edgecolor='white', label='Diameters Selected (Excluding Uncertain Contours)')
    ax2.set_xlabel('Grain Diameters (\u03BCm)')
    ax2.set_ylabel('Count of Grains')
    ax2.set_title(f'{grain_or_void} diameter histogram')

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


# draws contour lines on the original image
def draw_contours(image, grain_contours):

    # Copy the original image to edit
    result_image = image.copy()

    # Inverted grayscale image
    # result_image = cv2.bitwise_not(result_image)

    # Draws contour lines over the copied image
    cv2.drawContours(result_image, grain_contours, -1, (255, 0, 0), contour_thickness)  # Blue. Thickness 10

    return result_image


def display_images(watershed_imaged, outlined_image_cv, distance_transform_thresholded, original_image, thresholded_image_3chan, distance_transform):

    # Note if grain or void counting
    grain_or_void = count_type()

    fig, ((ax1, ax2, ax3), (ax4, ax5, ax6)) = plt.subplots(2, 3, figsize=(12, 8), sharex='all', sharey='all')
    fig.canvas.mpl_connect('button_press_event', on_press)
    fig.canvas.mpl_connect('button_release_event', on_release)

    ax5.imshow(watershed_imaged, cmap='gray')
    ax5.set_title(f'{grain_or_void} counting: Segment Separation')
    ax5.axis('off')
    Cursor(ax5, useblit=True, color='red', linewidth=1)

    ax6.imshow(cv2.cvtColor(outlined_image_cv, cv2.COLOR_BGR2RGB))
    ax6.set_title(f'{grain_or_void} counting: Contour Outlines')
    ax6.axis('off')
    Cursor(ax6, useblit=True, color='red', linewidth=1)

    ax4.imshow(cv2.cvtColor(distance_transform_thresholded, cv2.COLOR_BGR2RGB))
    ax4.set_title(f'{grain_or_void} counting: Binary Distance Transform')
    ax4.axis('off')
    Cursor(ax4, useblit=True, color='red', linewidth=1)

    ax1.imshow(cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB))
    ax1.set_title(f'{grain_or_void} counting: Original Image')
    ax1.axis('off')
    Cursor(ax1, useblit=True, color='red', linewidth=1)

    ax2.imshow(cv2.cvtColor(thresholded_image_3chan, cv2.COLOR_BGR2RGB))
    ax2.set_title(f'{grain_or_void} counting: Binary Thresholded Contrast')
    ax2.axis('off')
    Cursor(ax2, useblit=True, color='red', linewidth=1)

    ax3.imshow(cv2.cvtColor(distance_transform, cv2.COLOR_BGR2RGB))
    ax3.set_title(f'{grain_or_void} counting: Distance Transform')
    ax3.axis('off')
    Cursor(ax3, useblit=True, color='red', linewidth=1)

    plt.tight_layout()
    plt.show()


def run_grain_counting():
    init_GUI_variables()
    grain_or_void = count_type()
    thresholded_image_3chan, markers, image, dtt, dt = load_and_preprocessing()
    watershed_image = watershed_and_postprocessing(thresholded_image_3chan, markers)
    contour_area_total, grain_average_diameter_real, grain_contours, grain_average_area_mm, pixel_size_mm, grain_areas, grain_diameters, grain_areas_filtered, grain_diameters_filtered = calculate_area_and_filter_contours(watershed_image)

    if show_hist:
        grain_size_histogram(grain_areas_filtered, grain_diameters_filtered)

    contoured_image = draw_contours(image, grain_contours)

    if watershed_image is not None and contoured_image is not None:

        print(f"------------------------------------------------------------------------------------------------------")
        print(f"------------------------------------------------------------------------------------------------------")
        print(f"IMAGE PATH: {image_path}")
        print(f" ")
        print(f"-----------")
        print(f"{grain_or_void.upper()} COUNT")
        print(f"-----------")
        print(
            f"Number of {grain_diameter_min:.3f} mm to {grain_diameter_max:.3f} mm {grain_or_void}s visible: "
            f"{len(grain_contours)}")
        print(f" ")
        print(f"----------")
        print(f"{grain_or_void.upper()} AREA")
        print(f"----------")
        print(f"Total surface area of contoured regions: {contour_area_total:.3f} mm\u00b2")
        print(
            f"Average visible surface area of the {grain_diameter_min:.3f} mm to {grain_diameter_min:.3f} mm "
            f"{grain_or_void}s: {grain_average_area_mm:.3f} mm\u00b2")
        print(f" ")
        print(f"--------------")
        print(f"{grain_or_void.upper()} DIAMETER")
        print(f"--------------")
        print(
            f"Average diameter of {grain_diameter_min:.3f} mm to {grain_diameter_max:.3f} mm "
            f"{grain_or_void}s: {grain_average_diameter_real:.3f} mm")
        print(f" ")
        print(f"---------------------------")
        print(f"IMAGE PROCESSING PARAMETERS")
        print(f"---------------------------")
        print(f'Scale Factor: {scale_factor}')
        print(f'Scale Bar Pixels Per mm: {scale_bar_pixels_per_mm}')
        print(f'Bottom Crop Ratio: {bottom_crop_ratio}')
        print(f'Histogram Bins: {histogram_bins}')
        print(f'Contour Thickness: {contour_thickness}')
        print(f'Count Voids: {count_voids}')
        print(f'Equalize Histogram: {equalize_hist}')
        print(f'Lower Grayscale Threshold: {grayscale_threshold_lower}')
        print(f'Upper Grayscale Threshold: {grayscale_threshold_upper}')
        print(f'Kernel Size: {kernel_size}')
        print(f'Distance Threshold: {distanceTransform_threshold}')
        print(f'{grain_or_void.title()} Morphology Simplicity: {grain_morphology}')
        print(f'{grain_or_void.title()} Area|Diameter Min: {grain_area_min * pixel_size_mm} mm\u00b2 | {grain_diameter_min:.3f} mm')
        print(f'{grain_or_void.title()} Area|Diameter Max: {grain_area_max * pixel_size_mm} mm\u00b2 | {grain_diameter_max:.3f} mm')
        print(f"------------------------------------------------------------------------------------------------------")
        print(f"------------------------------------------------------------------------------------------------------")

        if show_images:
            display_images(watershed_image, contoured_image, dtt, image, thresholded_image_3chan, dt)

    else:
        print("Error: Unable to process images.")
        sys.exit()


def reset_values():
    config_watershedAll.scale_factor.set(1.0)
    config_watershedAll.scale_bar_pixels_per_mm.set(255.9812)
    config_watershedAll.bottom_crop_ratio.set(0.05)

    config_watershedAll.histogram_bins.set(20)
    config_watershedAll.contour_thickness.set(10)

    config_watershedAll.grayscale_threshold_lower.set(170)
    config_watershedAll.grayscale_threshold_upper.set(255)
    config_watershedAll.kernel_size.set(3)
    config_watershedAll.distanceTransform_threshold.set(7)
    config_watershedAll.grain_morphology.set(3)

    config_watershedAll.grain_area_min.set(0.283)
    config_watershedAll.grain_diameter_min.set(0.600)
    config_watershedAll.grain_area_max.set(0.763)
    config_watershedAll.grain_diameter_max.set(1.180)