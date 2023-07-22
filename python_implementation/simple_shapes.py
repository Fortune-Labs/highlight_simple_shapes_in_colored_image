import cv2
import numpy as np

# Function to highlight simple shapes of a given color in an image
def highlight_shapes_of_color(image_path, target_color):
    # Step 1: Read the input image
    original_image = cv2.imread(image_path)
    
    # Step 2: Convert the image from BGR to HSV color space
    hsv_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2HSV)
    
    # Step 3: Threshold the image based on the hue value to isolate the pixels of the given color
    target_color_hsv = cv2.cvtColor(np.uint8([[target_color]]), cv2.COLOR_BGR2HSV)[0][0]
    hue_tolerance = 10  # Adjust this value to control the sensitivity to the target color
    lower_bound = np.array([target_color_hsv[0] - hue_tolerance, 100, 100], dtype=np.uint8)
    upper_bound = np.array([target_color_hsv[0] + hue_tolerance, 255, 255], dtype=np.uint8)
    color_mask = cv2.inRange(hsv_image, lower_bound, upper_bound)
    
    # Step 4: Find contours in the thresholded image
    contours, _ = cv2.findContours(color_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Step 5: Highlight the detected shapes in the original image
    highlighted_image = original_image.copy()
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 50:  # Filter out small noise contours (adjust the threshold as needed)
            cv2.drawContours(highlighted_image, [contour], -1, (0, 0, 255), 2)  # Draw red contour on the original image
    
    # Display the result
    cv2.imshow("Original Image", original_image)
    cv2.imshow("Highlighted Shapes", highlighted_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Example usage
image_path = "path/to/your/image.jpg"  # Replace with the actual image path
target_color = (0, 0, 255)  # Red color in BGR format (adjust the values for other colors)

highlight_shapes_of_color(image_path, target_color)
