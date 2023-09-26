// Collect input values
var scaleToPixelRatio = document.getElementById('scale-to-pixel-ratio').value;  
var bottomCropRatio = document.getElementById('bottom-crop-ratio').value;
var showSizeHistogram = document.getElementById('show-size-histogram').value;
var segmentationImages = document.getElementById('segmentation-images').value;
var histogramBins = document.getElementById('histogram-bins').value;
var contourThickness = document.getElementById('contour-thickness').value;
var segmentationImages = document.getElementById('segmentation-images').value;
var histogramEqualisation = document.getElementById('histogram-equalisation').value;
var lowerContrastThreshold = document.getElementById('lower-contrast-threshold').value;
var upperContrastThreshold = document.getElementById('upper-contrast-threshold').value;
var blurKernelSize = document.getElementById('blur-kernel-size').value;
var distanceTransform = document.getElementById('distance-transform').value;
var morphologySimplicity = document.getElementById('morphology-simplicity').value;
var minSizeDiameter = document.getElementById('min-size-diameter').value;
var minSizeArea = document.getElementById('min-size-area').value;
var maxSizeDiameter = document.getElementById('max-size-diameter').value;
var maxSizeArea = document.getElementById('max-size-area').value;

// INclude input values in POST request
fetch('/run', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
    'scale-to-pixel-ratio': scaleToPixelRatio,
    'bottom-crop-ratio': bottomCropRatio,
    'show-size-histogram': showSizeHistogram,
    'segmentation-images': segmentationImages,
    'histogram-bins': histogramBins,
    'contour-thickness': contourThickness,
    'segmentation-images': segmentationImages,
    'histogram-equalisation': histogramEqualisation,
    'lower-contrast-threshold': lowerContrastThreshold, 
    'upper-contrast-threshold': upperContrastThreshold,
    'blur-kernel-size': blurKernelSize,
    'distance-transform': distanceTransform,
    'morphology-simplicity': morphologySimplicity,
    'min-size-diameter': minSizeDiameter,
    'min-size-area': minSizeArea,
    'max-size-diameter': maxSizeDiameter,
    'max-size-area': maxSizeArea
    })
})