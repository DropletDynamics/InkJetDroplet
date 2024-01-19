import cv2
import numpy as np
import operator # for sorting and comparing

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

def process_image(img):   
    # convert to gray
    gray = img#cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # threshold
    thresh = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY)[1]

    # morphology edgeout = dilated_mask - mask
    # morphology dilate
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5,5))
    dilate = cv2.morphologyEx(thresh, cv2.MORPH_DILATE, kernel)
    

    # get absolute difference between dilate and thresh
    # diff = cv2.absdiff(dilate, thresh)

    # invert
    # edges = 255 - diff

    # write result to disk
    # cv2.imwrite("process"+"/"+file+"_thresh.jpg", thresh)
    # cv2.imwrite("process"+"/"+file+"_dilate.jpg", dilate)
    # cv2.imwrite("process"+"/"+file+"_diff.jpg", diff)
    # cv2.imwrite("process"+"/"+file+"_edges.jpg", edges)

    # # display it
    # cv2.imshow("thresh", thresh)
    # cv2.imshow("dilate", dilate)
    # cv2.imshow("diff", diff)
    # cv2.imshow("edges", edges)
    # cv2.waitKey(0)
    return dilate# diff# edges

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
    
def get_centroid(contour):
    M = cv2.moments(contour)
    if M['m00'] != 0:
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])        
    else:
        # Handle the case where the contour is a line or a point
        # by taking the first point of the contour
        cx, cy = contour[0][0]
        
    return (cx, cy)

# This function samples points along the line connecting c1 and c2, checks their intensity, and returns the coordinates of the darkest point
def find_darkest_point(img, c1, c2):
    # Create a line iterator for the line between c1 and c2
    line_iterator = cv2.LineIterator(img, c1, c2, 8)
    
    # Initialize variables to store the darkest point and its intensity
    darkest_point = None
    min_intensity = 255  # Assuming 8-bit grayscale image
    
    # Iterate over the points in the line
    for point in line_iterator:
        # Get the intensity of the current point
        intensity = img[point[0][1], point[0][0]]
        
        # Update the darkest point if the current intensity is lower
        if intensity < min_intensity:
            min_intensity = intensity
            darkest_point = (point[0][0], point[0][1])
    
    return darkest_point

# Function for splitting a contour at a given point
def split_contour_at_point(contour, split_point):
    # Find the index of the contour point closest to the split_point
    distances = np.sqrt((contour[:, :, 0] - split_point[0]) ** 2 + (contour[:, :, 1] - split_point[1]) ** 2)
    min_distance_index = np.argmin(distances)
    
    # Split the contour into two parts at the index
    contour_part1 = contour[:min_distance_index]
    contour_part2 = contour[min_distance_index:]
    
    # Return the two new contours
    return contour_part1, contour_part2


# Function to check the gradient change
def check_gradient(image, contour):
    # Find the centroid or a point inside the contour
    M = cv2.moments(contour)
    if M['m00'] != 0:
        cx = int(M['m10'] / M['m00'])
        cy = int(M['m01'] / M['m00'])
    else:
        # Handle the case where the contour is a line or a point
        # by taking the first point of the contour
        cx, cy = contour[0][0]

    # Define the step size for moving towards the boundary
    step_size = 1

    # Move towards the boundary of the contour
    for i in range(0, len(contour), step_size):
        point = contour[i][0]
        x, y = point

        # Check the color intensity at the current point
        intensity_centroid = image[cy][cx]
        intensity_boundary = image[y][x]

        # Check for gradient change from white to dark
        if intensity_boundary < intensity_centroid:
            # Gradient change detected, accept the contour
            return True

    # No gradient change detected, reject the contour
    return False

def apply_fourier_transform(gray_image):
    # Load the image in grayscale
    # image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # Apply 2D Discrete Fourier Transform (DFT)
    dft = cv2.dft(np.float32(gray_image), flags=cv2.DFT_COMPLEX_OUTPUT)
    dft_shift = np.fft.fftshift(dft)

    # Create a mask with high-pass filter (1s in the corners, 0s in the center)
    rows, cols = gray_image.shape
    crow, ccol = rows // 2, cols // 2
    mask = np.ones((rows, cols, 2), np.uint8)
    r = 10  # Radius of the low frequencies to block
    center = [crow, ccol]
    x, y = np.ogrid[:rows, :cols]
    mask_area = (x - center[0]) ** 2 + (y - center[1]) ** 2 <= r*r
    mask[mask_area] = 0

    # Apply the mask to the shifted DFT
    fshift = dft_shift * mask

    # Inverse DFT to get the image back
    f_ishift = np.fft.ifftshift(fshift)
    img_back = cv2.idft(f_ishift)
    img_back = cv2.magnitude(img_back[:, :, 0], img_back[:, :, 1])

    # Normalize the image for display
    cv2.normalize(img_back, img_back, 0, 255, cv2.NORM_MINMAX)
    img_back = np.uint8(img_back)

    # Display the original and processed images
    # cv2.imshow('Original Image', image)
    # cv2.imshow('Image after High-Pass Filter', img_back)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    # cv2.imwrite("process"+"/"+image_path+'_fourier.jpg', img_back)

    return img_back

# A new function that uses Distance Transform
def split_contour(img_gray, contour, image_path="", index=0):
    # Create a binary image from the contour
    # img = np.zeros((480, 640), dtype=np.uint8) # Adjust the size according to your image
    img = np.zeros_like(img_gray)
    cv2.drawContours(img, [contour], -1, 255, -1)
    
    # Apply Distance Transform to the image
    dist = cv2.distanceTransform(img, cv2.DIST_L2, 3)
    cv2.normalize(dist, dist, 0, 255.0, cv2.NORM_MINMAX)
    dist = dist.astype(np.uint8)
    # cv2.imwrite("process"+"/"+image_path+str(index)+'_distanceTransform.jpg', dist)
    
    # Apply a threshold and a dilation to the distance image
    thresh = cv2.threshold(dist, 50, 255, cv2.THRESH_BINARY)[1] # Adjust the threshold value according to your image
    kernel = np.ones((9, 9), dtype=np.uint8) # Adjust the kernel size according to your image
    dilated = cv2.dilate(thresh, kernel)
    # cv2.imwrite("process"+"/"+image_path+str(index)+'_split_contour.jpg', dilated)
    
    # Find the two contours from the dilated image
    contours, hierarchy = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # if len(contours) != 2:
    #     print("Could not find two ellipses")
    #     return None, None
    
    # # Fit an ellipse to each contour
    # ellipse1 = cv2.fitEllipse(contours[0])
    # ellipse2 = cv2.fitEllipse(contours[1])
    
    # Return the two ellipses
    return contours, hierarchy#ellipse1, ellipse2

def contour_child_finder(contour_index, hierarchy):
    number_of_child = 0
    child_indexes = []
    child_index = hierarchy[0, contour_index, 2]
    while (child_index != -1):
        number_of_child += 1
        child_indexes.append(child_index)
        child_index = hierarchy[0, child_index, 0]        
        
    
    # Find the index of the current contour in the hierarchy
    # index = np.where(hierarchy[0, :, 2] == -1)[0][0]

    # Check if the current contour has a single child
    return number_of_child, child_indexes #hierarchy[0, index, 2] != -1


def measure_droplet_properties(edges, image_path=""):
    contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # print(hierarchy)

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
        # i = 0
        for i, contour in enumerate(contours): #while i < len(contours):
            # contour = contours[i]
            number_of_child, child_indexes = contour_child_finder(i, hierarchy)
            # print(f'Number of children for contour {i}: {number_of_child}')
            if number_of_child>1:
                cnts, hiers = split_contour(edges, contour, image_path, i)
                for cnt in cnts:
                    if len(cnt) >= 5:
                        # Calculate area of the contour
                        area = cv2.contourArea(cnt)
                        perimeter = cv2.arcLength(cnt, False)
                        # print(contour)

                        # Fit an ellipse to the contour to get semi-axes
                        ellipse = cv2.fitEllipseDirect(cnt)
                        if ellipse is not None:

                            major_axis, minor_axis = ellipse[1]
                        # print(f'Major Axis: {major_axis}, Minor Axis: {minor_axis}, Angle: {ellipse[2]}')
                            area_ellipse = np.pi * (major_axis/2) * (minor_axis/2)
                            perimeter_ellipse = 2.0 * np.pi * np.sqrt(((major_axis/2)**2 + (minor_axis/2)**2)/2.0)
                            if area_ellipse > 0 and area > 0:
                                area_ratio = area_ellipse/area
                                perimeter_ratio = perimeter_ellipse/perimeter
                            # print(area_ratio, perimeter_ratio)
                                if np.abs(area_ratio-1) < 0.2 or np.abs(perimeter_ratio-1) < 0.2:#
                                    ellipses.append(ellipse)
                # print(f"Contour {i} has more than one child")
            elif number_of_child==1:
                # print(f"Contour {i} has a single child")
                if len(contour) >= 5:
                    # Calculate area of the contour
                    area = cv2.contourArea(contour)
                    perimeter = cv2.arcLength(contour, False)
                    # print(contour)

                    # Fit an ellipse to the contour to get semi-axes
                    ellipse = cv2.fitEllipseDirect(contour)
                    if ellipse is not None:

                        major_axis, minor_axis = ellipse[1]
                    # print(f'Major Axis: {major_axis}, Minor Axis: {minor_axis}, Angle: {ellipse[2]}')
                        area_ellipse = np.pi * (major_axis/2) * (minor_axis/2)
                        perimeter_ellipse = 2.0 * np.pi * np.sqrt(((major_axis/2)**2 + (minor_axis/2)**2)/2.0)
                        if area_ellipse > 0 and area > 0:
                            area_ratio = area_ellipse/area
                            perimeter_ratio = perimeter_ellipse/perimeter
                            # print(area_ratio, perimeter_ratio)
                            if np.abs(area_ratio-1) < 0.2 or np.abs(perimeter_ratio-1) < 0.2:#
                                ellipses.append(ellipse)
            

        return contours, hierarchy, ellipses# major_axis, minor_axis,

        
    else:
        return None, 0, None 
    
def draw_contours_with_different_colors(img, contours):
    # Draw each contour with a different color
    for i, contour in enumerate(contours):
        color = tuple(np.random.randint(0, 255, 3).tolist())
        cv2.drawContours(img, [contour], -1, color, 2)

    # Return the image with the contours
    return img

def ellipses_analysis(ellipses):
    
    if ellipses:
        # Define a lambda function that returns the area of an ellipse
        area = lambda e: e[1][0] * e[1][1]
        # Sort the list of ellipses by area in descending order
        ellipses_sorted = sorted(ellipses, key=area, reverse=True)        
        n = len(ellipses)
        properties = []
        for ellipse in ellipses_sorted:        
            major_axis, minor_axis = ellipse[1]
            angle = ellipse[2]
            properties.append((major_axis, minor_axis, angle))        
    else:
        n = 0
        properties = [(0,0,0)]
    return n, properties

def droplet_boundary(image_path):

    # Load the image
    image = cv2.imread(image_path)
    
    
    # edges = process_image(image)
    # cv2.imwrite("process"+"/"+image_path+'_morphology.jpg', edges)
    # # convert to gray
    # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # ft_image = apply_fourier_transform(gray)
    # # # threshold
    # thresh =  ft_image#cv2.adaptiveThreshold(ft_image,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,2)#cv2.threshold(ft_image, 2, 255, cv2.THRESH_BINARY)[1]
    # thresh = process_image(ft_image)
    
    # Crop and remove nozzle
    x_offset = 220#580
    y_offset = 0#485
    cropped_image = crop_and_remove_nozzle(image.copy(), x_offset, y_offset)
    
    # Enhance contrast
    image_contrast = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)#enhance_contrast(cropped_image)#cv2.GaussianBlur(image, (5, 5), 0)#

    
    
    # Detect droplet boundary
    # edges = detect_droplet_boundary(image_contrast)
    edges = process_image(image_contrast)
    
    # measure_nozzle_diameter(edges)

    # Measure droplet properties  largest_contour, area, 
    contours, hierarchy, ellipses = measure_droplet_properties(edges, image_path)

    # Draw fitted ellipse on the original image
    # image_with_ellipse = cropped_image.copy()
    # for ellipse in ellipses:
        # _ellipse = list(ellipse)
        # _centre = list(_ellipse[0])
        # _centre[0] = _centre[0] + x_offset # add x offset to draw ellipse in original image coordinates
        # _centre[1] = _centre[1] + y_offset # add x offset to draw ellipse in original image coordinates
        # _ellipse[0] = tuple(_centre) # update ellipse centre
        # ellipse = tuple(_ellipse)
        # cv2.ellipse(image_with_ellipse, ellipse, (0, 255, 0), 2)
        # print(f'Major Axis: {ellipse[1][1]}, Minor Axis: {ellipse[1][0]}, Angle: {ellipse[2]}')


    # Save the output figures
    # cv2.imwrite(image_path+'enhanced_contrast.jpg', image_contrast)
    # cv2.imwrite("process"+"/"+image_path+'_thresh.jpg', thresh)
    # cv2.imwrite("process"+"/"+image_path+'_Canny.jpg', edges)
    # cv2.imwrite("process"+"/"+image_path+'_ellipses.jpg', image_with_ellipse)
    # image_with_contours = cropped_image.copy()
    # cv2.drawContours(image_with_contours, contours, -1, (255, 0, 0), 2)
    # draw_contours_with_different_colors(image_with_contours, contours)
    # cv2.imwrite("process"+"/"+image_path+'_contours.jpg', image_with_contours)

    # # Set up the detector with default parameters.
    # detector = cv2.SimpleBlobDetector()    
    # # Detect blobs.
    # keypoints = detector.detect(image)    
    # # Draw detected blobs as red circles.
    # # cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures the size of the circle corresponds to the size of blob
    # im_with_keypoints = cv2.drawKeypoints(image, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    # cv2.imwrite("process"+"/"+image_path+'_keypoints.jpg', im_with_keypoints)
    

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
