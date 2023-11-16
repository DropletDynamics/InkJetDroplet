import cv2
import numpy as np

def enhance_contrast(image):
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    return clahe.apply(gray)

def crop_and_remove_nozzle(image, x_offset=150):
    cropped = image[:, x_offset:]  # Crop the right side of the image
    return cropped

def detect_droplet_boundary(image):
    # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(image, 50, 150)
    return edges

def measure_droplet_properties(edges):
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        # Assuming the largest contour corresponds to the droplet
        largest_contour = max(contours, key=cv2.contourArea)

        # Calculate area of the droplet
        area = cv2.contourArea(largest_contour)

        # Fit an ellipse to the contour to get semi-axes
        ellipse = cv2.fitEllipse(largest_contour)
        print(ellipse)
        print(type(ellipse[0][0]))
        # major_axis, minor_axis = ellipse[1]

        return largest_contour, area, ellipse# major_axis, minor_axis, 
    else:
        return None, 0, None 

def droplet_boundary(image_path):

    # Load the image
    image = cv2.imread(image_path)

    # Enhance contrast
    image_contrast = enhance_contrast(image.copy())

    # Crop and remove nozzle
    x_offset = 580
    cropped_image = crop_and_remove_nozzle(image_contrast.copy(), x_offset)

    # Detect droplet boundary
    edges = detect_droplet_boundary(cropped_image.copy())

    # Measure droplet properties
    largest_contour, area, ellipse = measure_droplet_properties(edges)

    # Draw fitted ellipse on the original image
    image_with_ellipse = image.copy()
    _ellipse = list(ellipse)
    _centre = list(_ellipse[0])
    _centre[0] = _centre[0] + x_offset # add x offset to draw ellipse in original image coordinates
    _ellipse[0] = tuple(_centre) # update ellipse centre
    ellipse = tuple(_ellipse)
    cv2.ellipse(image_with_ellipse, ellipse, (0, 255, 0), 2)


    # Save the output figures
    cv2.imwrite('enhanced_contrast.jpg', image_contrast)
    cv2.imwrite('cropped_image.jpg', cropped_image)
    cv2.imwrite('droplet_boundary.jpg', edges)
    cv2.imwrite('droplet_with_ellipse.jpg', image_with_ellipse)

    # Display the results
    # cv2.imshow('Original Image', image)
    # cv2.imshow('Enhanced Contrast', image_contrast)
    # cv2.imshow('Cropped Image', cropped_image)
    # cv2.imshow('Droplet Boundary', edges)
    # cv2.imshow('Droplet with Ellipse', image_with_ellipse)

    print(f'Droplet Area: {area}')
    print(f'Major Axis: {ellipse[1][1]}, Minor Axis: {ellipse[1][0]}, Angle: {ellipse[2]}')

    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

