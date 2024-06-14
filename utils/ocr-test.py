#!/bin/python
import cv2
import numpy as np
import matplotlib.pyplot as plt

def check_image_contains_template(source_path, template_path, threshold=0.8):
    # Read the source image and the template image
    source_img = cv2.imread(source_path, cv2.IMREAD_GRAYSCALE)
    template_img = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
    
    # Check if images were loaded successfully
    if source_img is None or template_img is None:
        raise FileNotFoundError("Source or template image not found.")
    
    # Perform template matching
    result = cv2.matchTemplate(source_img, template_img, cv2.TM_CCOEFF_NORMED)
    
    # Find the location with the highest matching score
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    
    # Check if the best match exceeds the threshold
    if max_val >= threshold:
        match = True
        match_location = max_loc
    else:
        match = False
        match_location = None
    
    return match, match_location, max_val

# Paths to the images (you can modify these paths accordingly)
source_image_path = '/home/deck/.steam/steam/appcache/librarycache/207650_header.jpg'
template_image_path = '/home/deck/.steam/steam/appcache/librarycache/207650_library_600x900.jpg'

# Perform the check
match, location, score = check_image_contains_template(source_image_path, template_image_path)

# Display the results
print(f"Template found: {match}")
if match:
    print(f"Location: {location}")
    print(f"Matching score: {score}")
else:
    print("Template not found.")
