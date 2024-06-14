#!/bin/python

# Load the images
large_image_path = 'large_image.jpg'
small_image_path = 'small_image.jpg'

large_image = cv2.imread(large_image_path)
small_image = cv2.imread(small_image_path)

# Convert images to grayscale
large_gray = cv2.cvtColor(large_image, cv2.COLOR_BGR2GRAY)
small_gray = cv2.cvtColor(small_image, cv2.COLOR_BGR2GRAY)

# Template matching to find the small image in the large image
result = cv2.matchTemplate(large_gray, small_gray, cv2.TM_CCOEFF_NORMED)
min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

# Get the coordinates of the found location
top_left = max_loc
h, w = small_gray.shape

# Extract the region of interest from the large image
roi = large_image[top_left[1]:top_left[1] + h, top_left[0]:top_left[0] + w]

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
