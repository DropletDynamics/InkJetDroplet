# Import the modules
import cv2
import glob
import time
import re
import h5py # for HDF5 format
import droplet_boundary_detect
import numpy as np # for array operations
import operator # for sorting and comparing
import sys
import csv

# Define the folder path and the file pattern
folder = "captures"#"selected"#_main
pattern = "images_V1-*_V2-*_V3-*_w1-*_w2-*_w3-*_d1-*_d2-*.jpg"

# Get the list of image files
files = glob.glob(folder + "/" + pattern)
print(f"Found {len(files)} image files matching the pattern")


# Create a HDF5 file named "results.hdf5" in write mode
# with h5py.File("results.hdf5", "w") as f:
    # Create a custom dtype that can store a variable number of floats
    # vlen_float = h5py.special_dtype(vlen=np.dtype('float64'))
    # Create a dataset named "table" with a variable length and dtype
    # dset = f.create_dataset("table", shape=(0,), dtype=vlen_float)
with open('results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["V1", "V2", "V3", "w1", "w2", "w3", "d1", "d2", "n", "c_x", "c_y", "a", "b", "theta"])
    # Loop through the image files
    start_time = time.time()
    for i, file in enumerate(files):
        sys.stdout.write(f"\rProcessing image {i+1}/{len(files)}, time elapsed: {time.time() - start_time}")
            
        # Extract the input variables from the file name
        # vars = re.findall("-?\d+", file)
        # Convert the variables to floats
        # Use re.search to find the values of the parameters
        # pattern = r"images_V1-([-+]?\\d+)_V2-([-+]?\\d+)_V3-([-+]?\\d+)_w1-(\\d+)_w2-(\\d+)_w3-(\\d+)_d1-(\\d+)_d2-(\\d+).jpg"
        match = re.search("V1-([+-]?\\d+)_V2-([+-]?\\d+)_V3-([-+]?\\d+)_w1-(\\d+)_w2-(\\d+)_w3-(\\d+)_d1-(\\d+)_d2-(\\d+)", file)
        # If a match is found, extract the values using group method
        # print(match.groups())
        if match:
            V1 = match.group(1)
            V2 = match.group(2)
            V3 = match.group(3)
            w1 = match.group(4)
            w2 = match.group(5)
            w3 = match.group(6)
            d1 = match.group(7)
            d2 = match.group(8)
        vars = [V1, V2, V3, w1, w2, w3, d1, d2]
        vars = [float(v) for v in vars]
        # print(vars)
        # Read the image file
        # img = cv2.imread(file)
        # Detect the ellipses in the image
        ellipses = droplet_boundary_detect.droplet_boundary(file)
        n, properties, ellipses_sorted = droplet_boundary_detect.ellipses_analysis(ellipses)
        # if n > 0:
        # for ellipse in ellipses:
        #     image = cv2.imread(file)
        #     cv2.ellipse(image, ellipse, (0, 255, 0), 2)
        #     file_path = folder+f'/processed/images_V1-{V1}_V2-{V2}_V3-{V3}_w1-{w1}_w2-{w2}_w3-{w3}_d1-{d1}_d2-{d2}_ellipses.jpg'
        #     # print(f'Saving processed image to {file_path}')
        #     cv2.imwrite(file_path, image)
        # print(properties[0][0])
        
        writer.writerow([V1, V2, V3, w1, w2, w3, d1, d2,n,properties[0][0],properties[0][1],properties[0][2],properties[0][3],properties[0][4]])
        # Convert the ellipses to a NumPy array
        # ellipses = np.array(ellipses)
        # properties = np.array(properties)
        # print(properties.flatten())
        
        # Sort the ellipses by their area in descending order
        # The area is the last element of the tuple
        # ellipses = sorted(ellipses, key=operator.itemgetter(-1), reverse=True)
        # Get the size of the list of ellipses
        # Concatenate the input variables, n, and the list of ellipses along the first dimension
        # data = np.concatenate((vars, n, properties.flatten()), axis=0)
        # Resize the dataset to accommodate the new data
        # dset.resize(i + 1, axis=0)
        # Write the data to the dataset
        # dset[i] = data
        sys.stdout.flush()
    sys.stdout.write("\n")
