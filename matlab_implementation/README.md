# MATLAB SOLUTION

### MATLAB solution for highlighting simple shapes of a given color in multiple images, we can follow the steps outlined below:

* Read the input image.
* Convert the image from RGB to the HSV color space (Hue, Saturation, Value).
* Threshold the image based on the hue value to isolate the pixels of the given color.
* Perform shape detection on the thresholded image to identify simple shapes (e.g., circles, rectangles).
* Highlight the detected shapes in the original image.