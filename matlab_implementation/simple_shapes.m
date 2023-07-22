% Function to highlight simple shapes of a given color in an image
function highlightShapesOfColor(imagePath, targetColor)

    % Step 1: Read the input image
    originalImage = imread(imagePath);
    imshow(originalImage);
    title('Original Image');
    drawnow;
    
    % Step 2: Convert the image from RGB to HSV color space
    hsvImage = rgb2hsv(originalImage);
    
    % Step 3: Threshold the image based on the hue value to isolate the pixels of the given color
    targetHue = rgb2hsv(uint8([targetColor(1), targetColor(2), targetColor(3)]));
    hueTolerance = 0.05; % Adjust this value to control the sensitivity to the target color
    hueMask = (abs(hsvImage(:, :, 1) - targetHue(1)) < hueTolerance);
    
    % Step 4: Perform shape detection on the thresholded image
    binaryImage = hueMask; % For simplicity, we directly use the hue mask as the binary image
    binaryImage = imfill(binaryImage, 'holes'); % Fill any holes in the shapes
    
    % Step 5: Highlight the detected shapes in the original image
    highlightedImage = originalImage;
    highlightedImage(repmat(~binaryImage, [1, 1, 3])) = 0; % Set non-shape pixels to black
    
    % Display the result
    figure;
    subplot(1, 2, 1);
    imshow(originalImage);
    title('Original Image');
    subplot(1, 2, 2);
    imshow(highlightedImage);
    title('Highlighted Shapes');
    
end


% Example usage
imagePath = 'path/to/your/image.jpg'; % Replace with the actual image path
targetColor = [255, 0, 0]; % Red color (adjust the RGB values for other colors)

highlightShapesOfColor(imagePath, targetColor);
