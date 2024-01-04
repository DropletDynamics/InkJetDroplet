import cv2
import numpy as np

def enhance_contrast(image):
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    return clahe.apply(gray)

def crop_and_remove_nozzle(image, x_offset=0, y_offset=0):
    cropped = image[y_offset:, x_offset:]  # Crop the right side of the image
    return cropped

def detect_droplet_boundary(image):
    # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(image, (5, 5), 0)
    edges = cv2.Canny(gray, 50, 200)
    return edges

def measure_nozzle_diameter(edges):
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        image = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
        for contour in contours:
            # Get the minimum area rectangle that contains the contour
            rect = cv2.minAreaRect(contour)
    
            # Get the four vertices of the rectangle
            box = cv2.boxPoints(rect)
            box = np.int0(box)
    
            # Draw the rectangle on the original image
            
            cv2.drawContours(image, [box], -1, (255, 0, 0), 2)
            
            # Print the coordinates of the rectangle
            print(f"Rectangle found at {box.flatten().tolist()}")
            
        cv2.imwrite('droplet_boundary.jpg', image)

def contour_intersect(cnt_ref,cnt_query, edges_only = True):
    
    intersecting_pts = []
    
    ## Loop through all points in the contour
    for pt in cnt_query:
        x,y = pt[0]

        ## find point that intersect the ref contour
        ## edges_only flag check if the intersection to detect is only at the edges of the contour
        
        if edges_only and (cv2.pointPolygonTest(cnt_ref,(x,y),True) == 0):
            intersecting_pts.append(pt[0])
        elif not(edges_only) and (cv2.pointPolygonTest(cnt_ref,(x,y),True) >= 0):
            intersecting_pts.append(pt[0])
            
    if len(intersecting_pts) > 0:
        return True
    else:
        return False

def measure_droplet_properties(edges):
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:        
        # Assuming the largest contour corresponds to the droplet
        # largest_contour = max(contours, key=cv2.contourArea)
        # Calculate area of the droplet
        # area = cv2.contourArea(largest_contour)

        # # Fit an ellipse to the contour to get semi-axes
        # ellipse = cv2.fitEllipse(largest_contour)
        # print(ellipse)
        # print(type(ellipse[0][0]))
        # # major_axis, minor_axis = ellipse[1]

        # return largest_contour, area, ellipse# major_axis, minor_axis,
        ellipses = [] 
        for contour in contours:
            if len(contour) >= 5:
                # Calculate area of the contour
                area = cv2.contourArea(contour)
                perimeter = cv2.arcLength(contour, False)

                # Fit an ellipse to the contour to get semi-axes
                ellipse = cv2.fitEllipse(contour)
                if ellipse is not None:

                    major_axis, minor_axis = ellipse[1]
                    # print(f'Major Axis: {major_axis}, Minor Axis: {minor_axis}, Angle: {ellipse[2]}')
                    area_ellipse = np.pi * (major_axis/2) * (minor_axis/2)
                    perimeter_ellipse = 2.0 * np.pi * np.sqrt(((major_axis/2)**2 + (minor_axis/2)**2)/2.0)
                    if area_ellipse > 0 and area > 0:
                        area_ratio = area_ellipse/area
                        perimeter_ratio = perimeter_ellipse/perimeter
                        print(area_ratio, perimeter_ratio)
                        if np.abs(area_ratio-1) < 0.2 or np.abs(perimeter_ratio-1) < 0.2:#
                            ellipses.append(ellipse)
            

        return contours, ellipses# major_axis, minor_axis,

        
    else:
        return None, 0, None 

def droplet_boundary(image_path):

    # Load the image
    image = cv2.imread(image_path)

    # Enhance contrast
    image_contrast = enhance_contrast(image.copy())

    # Crop and remove nozzle
    x_offset = 0#580
    y_offset = 485
    cropped_image = crop_and_remove_nozzle(image_contrast.copy(), x_offset, y_offset)

    # Detect droplet boundary
    edges = detect_droplet_boundary(cropped_image.copy())

    # measure_nozzle_diameter(edges)

    # Measure droplet properties  largest_contour, area, 
    contours, ellipses = measure_droplet_properties(edges)

    # Draw fitted ellipse on the original image
    image_with_ellipse = image.copy()
    for ellipse in ellipses:
        _ellipse = list(ellipse)
        _centre = list(_ellipse[0])
        _centre[0] = _centre[0] + x_offset # add x offset to draw ellipse in original image coordinates
        _centre[1] = _centre[1] + y_offset # add x offset to draw ellipse in original image coordinates
        _ellipse[0] = tuple(_centre) # update ellipse centre
        ellipse = tuple(_ellipse)
        cv2.ellipse(image_with_ellipse, ellipse, (0, 255, 0), 2)
        print(f'Major Axis: {ellipse[1][1]}, Minor Axis: {ellipse[1][0]}, Angle: {ellipse[2]}')


    # Save the output figures
    cv2.imwrite(image_path+'enhanced_contrast.jpg', image_contrast)
    cv2.imwrite(image_path+'cropped_image.jpg', cropped_image)
    cv2.imwrite(image_path+'droplet_boundary.jpg', edges)
    cv2.imwrite(image_path+'droplet_with_ellipse.jpg', image_with_ellipse)
    image_with_contours = cropped_image.copy()
    cv2.drawContours(image_with_contours, contours, -1, (255, 0, 0), 2)
    cv2.imwrite(image_path+'droplet_with_contours.jpg', image_with_contours)

    # Display the results
    # cv2.imshow('Original Image', image)
    # cv2.imshow('Enhanced Contrast', image_contrast)
    # cv2.imshow('Cropped Image', cropped_image)
    # cv2.imshow('Droplet Boundary', edges)
    # cv2.imshow('Droplet with Ellipse', image_with_ellipse)

    # print(f'Droplet Area: {area}')

    

    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    
    return ellipses

# droplet_boundary('sattlite.jpg')#Captura0.PNG
