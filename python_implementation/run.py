import cv2
import os
import numpy as np

# Function to highlight and label pure deep colored objects with the target color in an image
def   highlight_and_label_colored_objects(image_path, target_color, save_path, min_area=200, max_area=5000, min_saturation=100, min_value=100):
    # Step 1: Read the input image
    original_image = cv2.imread(image_path)
    
    # Step 2: Convert the image from BGR to HSV color space
    hsv_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2HSV)
    
    # Step 3: Convert the target color from RGB to HSV format
    target_color_bgr = tuple(reversed(target_color))  # Convert RGB to BGR
    target_color_hsv = cv2.cvtColor(np.uint8([[target_color_bgr]]), cv2.COLOR_BGR2HSV)[0][0]
    
    # Step 4: Define the hue range for detecting the target color
    hue_tolerance = 15  # Adjust this value to control the sensitivity to the target color
    lower_bound = np.array([target_color_hsv[0] - hue_tolerance, min_saturation, min_value], dtype=np.uint8)
    upper_bound = np.array([target_color_hsv[0] + hue_tolerance, 255, 255], dtype=np.uint8)
    
    # Step 5: Threshold the image based on the hue, saturation, and value range to isolate the pixels of the given color
    color_mask = cv2.inRange(hsv_image, lower_bound, upper_bound)
    
    # Step 6: Find contours in the thresholded image
    contours, _ = cv2.findContours(color_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Step 7: Highlight and label pure deep colored objects with the target color
    highlighted_image = original_image.copy()
    for contour in contours:
        # Get the center of the object for placing the label
        moment = cv2.moments(contour)
        if moment["m00"] == 0:
            continue
        
        cX = int(moment["m10"] / moment["m00"])
        cY = int(moment["m01"] / moment["m00"])
        
        # Filter out small and large objects based on area
        area = cv2.contourArea(contour)
        if area < min_area or area > max_area:
            continue
        
        # Draw a rectangle around the object
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(highlighted_image, (x, y), (x + w, y + h), (0, 0, 255), 2)
        
        # Label the object with the target color name
        color_name = get_color_name(target_color)
        cv2.putText(highlighted_image, color_name, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    # Save the result
    cv2.imwrite(save_path, highlighted_image)

# Function to get the name of the color for the specific target color
def get_color_name(target_color):
    color_names = {
        (255, 0, 0): "Red",
        (0, 255, 0): "Green",
        (0, 0, 255): "Blue",
        (255, 255, 0): "Yellow",
        # Add more colors as needed
    }
    return color_names.get(target_color, "Unknown")

# Example usage for multiple images
input_folder = "D:\Others\Fabius\matlab\Shapes\highlight_simple_shapes_in_colored_image\images" # Replace with the folder path containing input images
output_folder = "D:\Others\Fabius\matlab\Shapes\highlight_simple_shapes_in_colored_image\output_image" # Replace with the folder path to save highlighted images
target_color = (0, 0, 255)  # Red color in RGB format (adjust the values for other colors)

# Loop through each image in the input folder
for filename in os.listdir(input_folder):
    if filename.endswith(".jpg") or filename.endswith(".png"):
        input_image_path = os.path.join(input_folder, filename)
        output_image_path = os.path.join(output_folder, f"highlighted_{filename}")
        highlight_and_label_colored_objects(input_image_path, target_color, output_image_path)
