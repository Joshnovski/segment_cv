<a name="readme-top"></a>

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/othneildrew/Best-README-Template">
    <img src="static/brand-white.png" alt="Logo" width="120" height="80">
  </a>

  <h3 align="center">S E G M E N T</h3>

  <p align="center">
    A computer vision web tool for segment characterisation.
    <br />
    <br />
    <br />
    <a href="https://segmentcv-deploy-e9a646f7dbd1.herokuapp.com/dashboard">View Demo</a>
    ·
    <a href="https://joshnovski.github.io/personal-website/">View Portfolio</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#about-the-project">About The Project</a></li>
    <li><a href="#built-with">Built With</a></li>
    <li>
      <a href="#usage">Usage</a>
      <ul>
        <li><a href="#authentication">Authentication</a></li>
        <li><a href="#dashboard">Dashboard</a></li>
        <li><a href="#control-panel">Control Panel</a></li>
        <li><a href="#scale-calculator">Scale Calculator</a></li>
        <li><a href="#results">Results</a></li>
        <li><a href="#account">Account</a></li>
        <li><a href="#surface-area-hist">Segment Surface Area Histogram</a></li>
        <li><a href="#diameter-approx-hist">Segment Diameter Approximation Histogram</a></li>
        <li><a href="#original-image">Original Image</a></li>
        <li><a href="#distance-transform">Distance Transform Image</a></li>
        <li><a href="#watershed">Watershed Segmentation Image</a></li>
        <li><a href="#contoured">Contoured Segments Image</a></li>
      </ul>
    </li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## [About The Project]()

[![Dashboard][product-screenshot]]()

SEGMENT is a computer vision web tool which utilises the OpenCV library to perform watershed segmentation of images. Contoured segments post-watershed are characterised by number and size, (where the size is calculated based on a pixel/mm scale). SEGMENT provides users with a control panel containing a number of image processing parameters which must be adjusted to improve segmentation accuracy. 

Segmentation results come in the form of a numerical results section, histograms, and processing stages of the uploaded image. The numerical results section contains values for the number of segments, the average segment surface area in mm<sup>2</sup> and the average diameter of the segment in mm which uses the assumption that the segments are mostly circular. The histogram plots illustrate the distribution of the segment surface areas and diameters. The processing stage images show the original uploaded image, the pixel distance transform of the grayscaled image, the post-watershed image and the contoured image, where each segment is outlined.

The watershed algorithm used in SEGMENT is a powerful image segmentation technique that is more thoughtful than other segmentation methods. It is widely used medical imaging and computer vision applications, and is a crucial step in many image processing pipelines. Despite its limitation, the watershed algorithm remains a popular choice for image segmentation tasks due to its ability to handle images with significant amounts of noise and irregular shapes.


<p align="right">(<a href="#readme-top">back to top</a>)</p>



## [Built With]()

* [![OpenCV][OpenCV.org]][OpenCV-url]
* [![Matplotlib][Matplotlib.org]][Matplotlib-url]
* [![NumPy][NumPy.org]][NumPy-url]
* [![SQLite][SQLite.org]][SQLite-url]
* [![Flask][Flask.py]][Flask-url]
* [![Figma][Figma.com]][Figma-url]
* [![Bootstrap][Bootstrap.com]][Bootstrap-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- USAGE EXAMPLES -->
## [Usage]()

#### [Authentication]()

Users will first be greeted with a login page consisting of login and sign-up options. Guest login details have been written in the placeholder location for the username and password. To get to the sign-up page, you must click the 'Sign up' link at the bottom of the login card. The Sign-up page allows users to craft an appropriate username and password to identify and secure their account. Users must confirm their password to ensure that no typos are introduced. Once registered, users are taken back to the login page where, once they sign in, they will be directed to the segmentation dashboard.

#### [Dashboard]()

The dashboard is divided into two sections. The section to the left is the navigation bar, or 'control panel', and the section to the right is the image output grid where size histograms and image processing steps are illustrated. Users will mostly interact with the control panel in order to upload images, adjust processing parameters, run the segmentation program and record sizing results. The images showing the segmentation steps are there so users can make appropriate parameter adjustments to improve segmentation quality.

#### [Control Panel]()

This is the main operations center for running and controlling the segmentation program. 

* [**Icons:**]() The First row of icons show an image icon, a reset icon and a play icon. The image icon allows users to select an image from their files, then a flash notification will tell the user when the upload process is complete. The reset icon, resets all variables to their default values. Lastly, the play icon runs the segmentation program, providing a flash notification once it is complete.
* [**Scale:**]() This value shows the result from the 'Scale Calculator' calculation as a ratio of pixels/mm.
* [**Histogram Bins:**]() The number of unit spacing groups along the x-axis. A higher bin number can highlight fine details in the distribution of groups but may sacrifice readability of the plot.
* [**Contour Thickness:**]() A scale value for the thickness of drawn contours seen in the 'Contoured Segments' image.
* [**Invert Grayscale:**]() Flips the values of each grayscaled pixel to the opposite end of the 256 value range. So if a pixel is black (0) it will become white (255). If the objects you want to segment are darker than the background, use this to ensure the objects are white and background is black.
* [**Histogram Equalisatio:**]() In the case where you need to improve the contrast of your grayscaled image, you can turn on histogram equalisation. This is an intensity transformation technique where you uniformly distribute the image histogram over the entire intensity axis. Details previously obscured may now be more readable for further image processing. A common practice in the medical industry to enhance contrast in X-ray, MRI and CT scan images.
* [**Contrast Threshold:**] Is a set of lower and upper boundary condition for a binary image transform. Pixels with brightness values within this are set to white (255), otherwise they are set to black (0). This is a way to only select the brightness range of objects you are interested in segmenting.
* [**Blue Kernel:**] Blur effects in image processing use a matrix where each pixel is a function of surrounding pixels in the matrix. The kernel defines the size of the matrix for which the a gaussian function is applied. The kernel must be odd, as the matrix must have a single center pixel. A 4x4 matrix for instance, has 4 pixels which make up the center, but a 3x3 matrix has only one pixel.
* [**Distance Transform:**] This value is an exclusion threshold for the distance transformed image. This is a used to divide connected regions of object in an image based on a pixels distance from black pixels. Higher values here will effectivly raise the water level (black background) in a pixel height map (distance transform). This process is visualised in the 'Distance Transform' Image. You want to set this value so that none of the objects you wish to count and characterise are touching.
* [**Morphology Simplicity:**] For higher resolution images, you can sometimes observe fine detailing and noise about your objects. To simplify and clean up the edges of your objects, you can raise this value. This may help reduce bridges between objects preventing them from being properly segmented.
* [**Segment Size:**] This is a size range selection where, if the scale is set corretly, users can specify which size range of segments they would like to have contoured and characterised in the results section.

#### [Scale Calculator]()

The scale calculator within the control panel allows users to quickly calculate and input the pixel/mm ratio needed to produce accurate size values for the segments. Users are required to have a scale bar or an object of known size in the image as a point of reference. Users are required to count the number of pixels corresponding to that known length and input the values in the input boxes. Pressing calculate will send the calculated ratio to the 'Control Center' menu as a parameter used in the running of the segmentation script. Later down the line, I would like to provide users with the ability to quickly count the distance in pixels by drawing a line on the image, but at the moment they may have to use a program like ImageJ or something similar.

#### [Results]()

Once an image has been processed and segmented, the results section shows the 'number of segments', the average surface area of the segments in mm<sup>2</sup> and the average diameter of the segments in mm. The diameter values are approximations taking the assumption that the segments are circular. If the segments are not circular, this value will be inaccurate.

#### [Account]()

In the account section of the control panel, users can only currently log out. Logging out will take the user back to the login screen. In the future, this section will allow users to access their profile where they can access all their previous saved results.

#### [Segment Surface Area Histogram]()

The surface area histogram allows users to see a distribution of the segmented areas. This plot relies on the user having input an accurate pixel/mm scale ratio.

#### [Segment Diameter Approximation Histogram]()

This histogram illustrates a distribution of segment diameters. These diameter values were calculated by assuming the segment is circular and then using the surface area to calculate its diameter. The surface area of a circle equation was sufficient for this, 'area = π(radius)<sup>2</sup>'. The assumption of a circular segment was made to make it easier to interpret the size of a segment. It is often easier to think about and understand a length than an area. Eventually when users are choosing the min and max size range to contour segments, they can better guage what kind of size they are expecting to observe if the boundary conditions are diameters in mm units rather than areas in mm<sup>2</sup> units. 

#### [Original Image]()

As expected from the name, this is the original image input by the user, unprocessed and in its original state.

#### [Distance Transform Image]()

The distance tranform of an image is calculated by counting the distance between a given pixel and its nearest black pixel, (a value of (0, 0, 0) on an RGB scale). This distance value is then assigned as the pixels brightness, so if a given pixel is far from a black pixel, the pixel will be more white. If the pixel is close to a black pixel, it will appear more gray. Effectivly this processing technique will turn a binary black and white image (0, 0, 0) and (255, 255, 255) respectivly, into 256 value range, grayscale image again.  Before this distance transform is peformed, the image is first grayscaled, then made binary with a threshold set by the user in the 'Control Center' tab. A distance transformed image acts as a height map where, given another threshold, users can 'raise the water level' so to speak. By changing the distance transform threshold, users exlude darker pixels from the height map with color values outside the threshold boundary. This is a technique used to divide connected regions of pixels in an image based on brightness, an important step in watershed segmentation.

#### [Watershed Segmentation Image]()

Watersheding is a image processing algorithm following from distance transforming. Any grayscale image can be viewed as a topographic map, where bright pixels are peaks and hills and darker pixels signify valleys. If you start filling every isolated valley (local minima) with different coloured water (labels), water from different valleys will start to merge. Where these different water pools merge, barriers (lines) are drawn. THis is repeated until all the peaks are under the water. These barriers give the segmentation results. However, this alone gives an oversegmented results, so OpenCV implemented a marker-based watershed algorithm. This allows you tp specify which valley points are to be merged and which are not. We give different lavels for objects we know, labeling regions we are sure of being the foreground with a colour, labeling the region which we are sure of being the background with another colour, and labelling the region we are not sure of anything with 0. This is our marker. The marker is then updated with the labels with gave and the boundaires of objects are given a value of -1. As with all image processing, it is never a sure science with how it will behave. For regions where separate objects in the image touch, they may be segmented properly and soe may not. Adjustments to the image processing parameters can be made to improve the results.

#### [Contoured Segments Image]()

This is the final image processing step where we draw contour lines along the boundaires of each segmented object. The user has access to change the thickness of these lines to make them more or less visible in the image.



<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[issues-shield]: https://img.shields.io/github/issues/othneildrew/Best-README-Template.svg?style=for-the-badge
[issues-url]: https://github.com/othneildrew/Best-README-Template/issues
[license-shield]: https://img.shields.io/github/license/othneildrew/Best-README-Template.svg?style=for-the-badge
[license-url]: https://github.com/othneildrew/Best-README-Template/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/othneildrew
[product-screenshot]: static/dashboard-pic.png
[Svelte.dev]: https://img.shields.io/badge/Svelte-4A4A55?style=for-the-badge&logo=svelte&logoColor=FF3E00
[Svelte-url]: https://svelte.dev/
[Laravel.com]: https://img.shields.io/badge/Laravel-FF2D20?style=for-the-badge&logo=laravel&logoColor=white
[Laravel-url]: https://laravel.com
[Bootstrap.com]: https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white
[Bootstrap-url]: https://getbootstrap.com
[Figma.com]: https://img.shields.io/badge/figma-%23F24E1E.svg?style=for-the-badge&logo=figma&logoColor=white
[Figma-url]: https://www.figma.com/
[Flask.py]: https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white
[Flask-url]: https://flask.palletsprojects.com/en/3.0.x/
[JavaScript.js]: https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E
[JavaScript-url]: https://www.w3schools.com/Js/
[CSS3.css]: https://img.shields.io/badge/css3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white
[CSS3-url]: https://www.w3schools.com/css/default.asp
[HTML5.html]: https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white
[HTML5-url]: https://www.w3schools.com/html/default.asp
[Python.org]: https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54
[Python-url]: https://www.python.org/
[SQLite.org]: https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white
[SQLite-url]: https://www.sqlite.org/index.html
[OpenCV.org]: https://img.shields.io/badge/opencv-%23white.svg?style=for-the-badge&logo=opencv&logoColor=white
[OpenCV-url]: https://opencv.org/
[Matplotlib.org]: https://img.shields.io/badge/Matplotlib-%23ffffff.svg?style=for-the-badge&logo=Matplotlib&logoColor=black
[Matplotlib-url]: https://matplotlib.org/
[NumPy.org]: https://img.shields.io/badge/numpy-%23013243.svg?style=for-the-badge&logo=numpy&logoColor=white
[NumPy-url]: https://numpy.org/
