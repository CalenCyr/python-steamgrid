#!/bin/python

import cv2
import pytesseract
from PIL import Image

# Load the images
large_image_path = '/home/deck/.steam/steam/appcache/librarycache/207650_header.jpg'
small_image_path = '/home/deck/.steam/steam/appcache/librarycache/207650_library_600x900.jpg'

large_image = cv2.imread(large_image_path)
small_image = cv2.imread(small_image_path)

# Check if images are loaded successfully
if large_image is None:
    raise ValueError(f"Failed to load the large image from {large_image_path}")
if small_image is None:
    raise ValueError(f"Failed to load the small image from {small_image_path}")

# Convert images to grayscale
large_gray = cv2.cvtColor(large_image, cv2.COLOR_BGR2GRAY)
small_gray = cv2.cvtColor(small_image, cv2.COLOR_BGR2GRAY)

# Template matching to find the small image in the large image
result = cv2.matchTemplate(large_gray, small_gray, cv2.TM_CCOEFF_NORMED)

# Get the best match position
min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

# Print debug information
print(f"Min value: {min_val}, Max value: {max_val}")
print(f"Min location: {min_loc}, Max location: {max_loc}")

# Check if the match is good enough
threshold = 0.8
if max_val < threshold:
    raise ValueError("No sufficiently good match found. Increase the threshold or check the images.")

# Get the coordinates of the found location
top_left = max_loc
h, w = small_gray.shape

# Check if the coordinates are within bounds
if top_left[1] + h > large_gray.shape[0] or top_left[0] + w > large_gray.shape[1]:
    raise ValueError("The found location is out of image bounds.")

# Extract the region of interest from the large image
roi = large_image[top_left[1]:top_left[1] + h, top_left[0]:top_left[0] + w]

# Check if ROI is valid
if roi.size == 0:
    raise ValueError("Extracted ROI is empty.")

# Convert the ROI and the small image to PIL format for pytesseract
roi_pil = Image.fromarray(cv2.cvtColor(roi, cv2.COLOR_BGR2RGB))
small_image_pil = Image.fromarray(cv2.cvtColor(small_image, cv2.COLOR_BGR2RGB))

# Perform OCR on both images
roi_text = pytesseract.image_to_string(roi_pil)
small_image_text = pytesseract.image_to_string(small_image_pil)

# Compare the extracted text
if small_image_text in roi_text:
    print("The smaller image is inside the larger image.")
else:
    print("The smaller image is NOT inside the larger image.")
