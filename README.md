<a name="readme-top"></a>

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/othneildrew/Best-README-Template">
    <img src="static/brand-cyan.png" alt="Logo" width="120" height="80">
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
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#usage">Usage</a>
      <ul>
        <li><a href="#authentication">Authentication</a></li>
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
## About The Project

[![Dashboard][product-screenshot]]()

SEGMENT is a computer vision web tool which utilises the OpenCV library to perform watershed segmentation of images. Contoured segments post watershed are characterised by number and size, (where the size is calculated based on a pixel/mm scale). SEGMENT provides users with a control panel containing a number of image processing parameters which must be adjusted to improve segmentation accuracy. 

Segmentation results come in the form of a numerical results section, histograms, and processing stages of the uploaded image. The numerical results section contains values for the number of segments, the average segment surface area in mm<sup>2</sup> and the average diameter of the segment in mm which uses the assumption that the segments are mostly circular. The histogram plots illustrate the distribution of the segment surface areas and diameters. The processing stage images show the original uploaded image, the pixel distance transform of the grayscaled image, the post watershed image and the contoured image, where each segment is outlined.


<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With

This section should list any major frameworks/libraries used to bootstrap your project. Leave any add-ons/plugins for the acknowledgements section. Here are a few examples.

* [![OpenCV][OpenCV.org]][OpenCV-url]
* [![Matplotlib][Matplotlib.org]][Matplotlib-url]
* [![NumPy][NumPy.org]][NumPy-url]
* [![SQLite][SQLite.org]][SQLite-url]
* [![Flask][Flask.py]][Flask-url]
* [![Figma][Figma.com]][Figma-url]
* [![Bootstrap][Bootstrap.com]][Bootstrap-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- USAGE EXAMPLES -->
## Usage

## Control Panel
<br />
<br />
## Scale Calculator
<br />
<br />
## Results
<br />
<br />
## Account
<br />
<br />
## Segment Surface Area Histogram
<br />
<br />
## Segment Diameter Approximation Histogram
<br />
<br />
## Original Image
<br />
<br />
## Distance Transform Image
<br />
<br />
## Watershed Segmentation Image
<br />
<br />
## Contoured Segments Image


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
