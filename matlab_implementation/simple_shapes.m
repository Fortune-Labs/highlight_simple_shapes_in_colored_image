function highlight_and_label_colored_objects(image_path, target_color, save_path, min_area, max_area, min_saturation, min_value)
    % Read the input image
    original_image = imread(image_path);
    
    % Convert the image from RGB to HSV color space
    hsv_image = rgb2hsv(original_image);
    
    % Convert the target color from RGB to HSV format
    target_color_rgb = target_color;
    target_color_hsv = rgb2hsv(reshape(target_color_rgb, 1, 1, 3));
    
    % Define the hue range for detecting the target color
    hue_tolerance = 0.15; % Adjust this value to control the sensitivity to the target color
    lower_bound = [target_color_hsv(1) - hue_tolerance, min_saturation/255, min_value/255];
    upper_bound = [target_color_hsv(1) + hue_tolerance, 1, 1];
    
    % Threshold the image based on the hue, saturation, and value range to isolate the pixels of the given color
    color_mask = (hsv_image(:,:,1) >= lower_bound(1)) & (hsv_image(:,:,1) <= upper_bound(1)) & ...
                 (hsv_image(:,:,2) >= lower_bound(2)) & (hsv_image(:,:,3) >= lower_bound(3));
    
    % Find connected components in the thresholded image
    labeled_image = bwlabel(color_mask);
    
    % Get region properties for connected components
    props = regionprops(labeled_image, 'Area', 'BoundingBox', 'Centroid');
    
    % Highlight and label colored objects with the target color
    highlighted_image = original_image;
    for i = 1:numel(props)
        % Filter out small and large objects based on area
        if props(i).Area < min_area || props(i).Area > max_area
            continue;
        end
        
        % Draw a rectangle around the object
        bounding_box = props(i).BoundingBox;
        highlighted_image = insertShape(highlighted_image, 'Rectangle', bounding_box, 'LineWidth', 2, 'Color', [0, 0, 255]);
        
        % Label the object with the target color name
        color_name = get_color_name(target_color_rgb);
        position = [bounding_box(1), bounding_box(2) - 10];
        highlighted_image = insertText(highlighted_image, position, color_name, 'FontSize', 12, 'TextColor', 'red', 'BoxOpacity', 0);
    end

    % Save the result
    imwrite(highlighted_image, save_path);
end

function color_name = get_color_name(target_color_rgb)
    color_names = containers.Map({[255, 0, 0], [0, 255, 0], [0, 0, 255], [255, 255, 0]}, ...
                                 {'Red', 'Green', 'Blue', 'Yellow'});
    color_name = color_names(mat2str(target_color_rgb));
    if isempty(color_name)
        color_name = 'Unknown';
    end
end

% Example usage for multiple images
input_folder = "D:\Others\Fabius\matlab\Shapes\highlight_simple_shapes_in_colored_image\images" # Replace with the folder path containing input images
output_folder = "D:\Others\Fabius\matlab\Shapes\highlight_simple_shapes_in_colored_image\output_image" # Replace with the folder path to save highlighted images
target_color = [0, 0, 255];  % Red color in RGB format (adjust the values for other colors)

% Loop through each image in the input folder
image_files = dir(fullfile(input_folder, '*.jpg'));
for i = 1:length(image_files)
    input_image_path = fullfile(input_folder, image_files(i).name);
    output_image_path = fullfile(output_folder, ['highlighted_', image_files(i).name]);
    highlight_and_label_colored_objects(input_image_path, target_color, output_image_path, 200, 5000, 100, 100);
end
