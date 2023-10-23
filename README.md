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
        <li><a href="#control-panel">Control Panel</a></li>
        <li><a href="#scale-calculator">Scale Calculator</a></li>
        <li><a href="#results">Results</a></li>
        <li><a href="#account">Account</a></li>
        <li><a href="#surface-area-hist">Segment Surface Area Histogram</a></li>
        <li><a href="#diameter-approx-hist">Segment Diameter Approximation Histogram</a></li>
        <li><a href="#original-image">Original Image</a></li>
        <li><a href="#distance-transform">Distance Transform Image</a></li>
        <li><a href="#watershed">Watershed Segmentation image</a></li>
        <li><a href="#contoured">Contoured Segments image</a></li>
      </ul>
    </li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

[![Product Name Screen Shot][https://www.bizinfograph.com/assets/uploads/primary_images/42/2895ff292fb596d9b8b88d49df971b78.JPG]](https://example.com)

SEGMENT is a computer vision web tool which utilises the OpenCV library to perform watershed segmentation of images. Contoured segments post watershed are characterised by number and size, (where the size is calculated based on a pixel/mm scale). SEGMENT provides users with a control panel containing a number of image processing parameters which must be adjusted to improve segmentation accuracy. 

Segmentation results come in the form of a numerical results section, histograms, and processing stages of the uploaded image. The numerical results section contains values for the number of segments, the average segment surface area in mm^2 and the average diameter of the segment in mm which uses the assumption that the segments are mostly circular. The histogram plots illustrate the distribution of the segment surface areas and diameters. The processing stage images show the original uploaded image, the pixel distance transform of the grayscaled image, the post watershed image and the contoured image, where each segment is outlined.


<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With

This section should list any major frameworks/libraries used to bootstrap your project. Leave any add-ons/plugins for the acknowledgements section. Here are a few examples.

* [![Flask][Flask.com]][Flask-url]
* [![JavaScript][JavaScript.com]][JavaScript-url]
* [![Python][Python.org]][Python-url]
* [![HTML][HTML.com]][HTML-url]
* [![CSS][CSS.com]][CSS-url]
* [![JavaScript][JavaScript.js]]
* [![Flask][Flask.py]][Flask-url]
* [![Figma][Figma.com]][Figma-url]
* [![Bootstrap][Bootstrap.com]][Bootstrap-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

This is an example of how you may give instructions on setting up your project locally.
To get a local copy up and running follow these simple example steps.

### Prerequisites

This is an example of how to list things you need to use the software and how to install them.
* npm
  ```sh
  npm install npm@latest -g
  ```

### Installation

_Below is an example of how you can instruct your audience on installing and setting up your app. This template doesn't rely on any external dependencies or services._

1. Get a free API Key at [https://example.com](https://example.com)
2. Clone the repo
   ```sh
   git clone https://github.com/your_username_/Project-Name.git
   ```
3. Install NPM packages
   ```sh
   npm install
   ```
4. Enter your API in `config.js`
   ```js
   const API_KEY = 'ENTER YOUR API';
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

Use this space to show useful examples of how a project can be used. Additional screenshots, code examples and demos work well in this space. You may also link to more resources.

_For more examples, please refer to the [Documentation](https://example.com)_

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[issues-shield]: https://img.shields.io/github/issues/othneildrew/Best-README-Template.svg?style=for-the-badge
[issues-url]: https://github.com/othneildrew/Best-README-Template/issues
[license-shield]: https://img.shields.io/github/license/othneildrew/Best-README-Template.svg?style=for-the-badge
[license-url]: https://github.com/othneildrew/Best-README-Template/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/othneildrew
[product-screenshot]: images/screenshot.png
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
