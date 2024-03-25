import glob
import re
import droplet_boundary_detect
import numpy as np # for array operations
import sys
import csv
import matplotlib.pyplot as plt

# Define the folder path and the file pattern
folder = "process/selected"#_main
pattern = "images_V1-*_V2-*_V3-*_w1-*_w2-*_w3-*_d1-*_d2-*.jpg"

# Get the list of image files
files = glob.glob(folder + "/" + pattern)
print(f"Found {len(files)} image files matching the pattern")


with open('.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["V1", "V2", "V3", "w1", "w2", "w3", "d1", "d2", "n", "a", "b", "theta"])
    # Loop through the image files
    for i, file in enumerate(files):
        sys.stdout.write(f"\rProcessing image {i+1}/{len(files)}")
            
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

        grad_x, grad_y, s1, s2 = droplet_boundary_detect.gradient_labeling(file)
        
        
        
        sys.stdout.flush()
    sys.stdout.write("\n")
