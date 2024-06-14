#!/bin/python

import cv2
import numpy as np
import matplotlib.pyplot as plt

def detect_blurred_background(image_path, blur_threshold=100):
    # Load the image
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError("Image not found.")
    
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Use a simple segmentation approach (e.g., thresholding) to separate foreground and background
    _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)
    
    # Apply morphological operations to clean up the segmentation
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
    
    # Find contours of the segmented regions
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Create a mask for the background
    background_mask = np.ones_like(gray) * 255
    cv2.drawContours(background_mask, contours, -1, (0), thickness=cv2.FILLED)
    
    # Extract the background region using the mask
    background = cv2.bitwise_and(gray, gray, mask=background_mask)
    
    # Compute the Laplacian of the background
    laplacian = cv2.Laplacian(background, cv2.CV_64F)
    
    # Compute the variance of the Laplacian
    laplacian_var = laplacian.var()
    
    # Determine if the background is blurred
    is_blurred = laplacian_var < blur_threshold
    
    return is_blurred, laplacian_var, background_mask, laplacian

def check_image_contains_template(source_path, template_path, threshold=0.5):
    # Read the source image and the template image
    source_img = cv2.imread(source_path, cv2.IMREAD_GRAYSCALE)
    template_img = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
    
    # Check if images were loaded successfully
    if source_img is None or template_img is None:
        raise FileNotFoundError("Source or template image not found.")

    # Check if template image is large than source image
    # Some "600x900" images Valve stores are not actually 600x900
    # To work around this, scale up the source image if it has that text in it
    # Because of this, the threshold should be more strict
    if template_img.shape[0] > source_img.shape[0] or template_img.shape[1] > source_img.shape[1]:
        msg = (f"Template image is larger than the source image.\nTemplate: {template_img.shape}\nSource: {source_img.shape}")
        if "600x900" in source_path:
            print(msg)
            print("Resizing to 600x900 per filename")
            threshold=2285905925
            source_img = cv2.resize(source_img, (600, 900), interpolation=cv2.INTER_AREA)
        else:
            raise ValueError(msg)

    # To avoid false positives, check if image is blurred
    # This is how the poor / improper capsules are made (wide background shrunk, blurred background)
    blurred = detect_blurred_background(source_path, blur_threshold=100)
    #print(f"Is image blurred?: {blurred}")
    if not blurred[0]:
        print("Image we are checking is not blurred, skipping")
        return False, "", "", ""
    
    # Perform template matching using different methods
    methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR', 'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']
    results = {}
    
    for method in methods:
        method_eval = eval(method)
        result = cv2.matchTemplate(source_img, template_img, method_eval)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        
        if method in ['cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']:
            match_val = min_val
            match_loc = min_loc
        else:
            match_val = max_val
            match_loc = max_loc
        
        results[method] = (match_val, match_loc)
    
    # Select the best match based on the highest score (or lowest for SQDIFF methods)
    best_method = max(results, key=lambda x: results[x][0] if 'SQDIFF' not in x else -results[x][0])
    best_match_val, best_match_loc = results[best_method]
    
    # Check if the best match exceeds the threshold
    print(f"Using threshold of: {threshold}")
    if best_match_val >= threshold if 'SQDIFF' not in best_method else best_match_val <= threshold:
        match = True
    else:
        match = False
    
    return match, best_match_loc, best_match_val, best_method

# Paths to the images (you can modify these paths accordingly)

# A Virus Named TOM 
# Should return true
#template_image_path = '/home/deck/.steam/steam/appcache/librarycache/207650_header.jpg'
#source_image_path = '/home/deck/.steam/steam/appcache/librarycache/207650_library_600x900.jpg'

# A Hat in Time
# Should return false
template_image_path = '/home/deck/.steam/steam/appcache/librarycache/253230_header.jpg'
source_image_path = '/home/deck/.steam/steam/appcache/librarycache/253230_library_600x900.jpg'

# Perform the check
match, location, score, method = check_image_contains_template(source_image_path, template_image_path)

# Display the results
print(f"Template found: {match}")
print(f"Best matching method: {method}")
if match:
    print(f"Location: {location}")
    print(f"Matching score: {score}")
else:
    print("Template not found.")

# Visualization
source_img = cv2.imread(source_image_path, cv2.IMREAD_GRAYSCALE)
template_img = cv2.imread(template_image_path, cv2.IMREAD_GRAYSCALE)
h, w = template_img.shape

if match:
    top_left = location
    bottom_right = (top_left[0] + w, top_left[1] + h)
    cv2.rectangle(source_img, top_left, bottom_right, 255, 2)

plt.figure(figsize=(10, 6))
plt.imshow(source_img, cmap='gray')
plt.title('Detected Template' if match else 'Template Not Found')
plt.show()
