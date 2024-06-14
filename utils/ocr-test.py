#!/bin/python

import cv2
import numpy as np
import matplotlib.pyplot as plt

def check_image_contains_template(source_path, template_path, threshold=0.5):
    # Read the source image and the template image
    source_img = cv2.imread(source_path, cv2.IMREAD_GRAYSCALE)
    template_img = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
    
    # Check if images were loaded successfully
    if source_img is None or template_img is None:
        raise FileNotFoundError("Source or template image not found.")
    
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
    if best_match_val >= threshold if 'SQDIFF' not in best_method else best_match_val <= threshold:
        match = True
    else:
        match = False
    
    return match, best_match_loc, best_match_val, best_method

# Paths to the images (you can modify these paths accordingly)
template_image_path = '/home/deck/.steam/steam/appcache/librarycache/207650_header.jpg'
source_image_path = '/home/deck/.steam/steam/appcache/librarycache/207650_library_600x900.jpg'

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
