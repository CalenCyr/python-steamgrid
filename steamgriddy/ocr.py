import cv2
import numpy as np
import matplotlib.pyplot as plt

# This function checks if the source image is in the target image
# * The template image would be the old wide banner Steam Big Picture 
# * The source image would be the one we are checking 
# * This effectively checks if the cover art is just a shrunk down wide banner with a blurred background
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

    return match

