# Import the modules
import glob
import sys
import time
import h5py
import re
import numpy as np

import droplet_boundary_detect


## Define the folder path and the file pattern
folder = "captures"#_main
pattern = "images_V1-*_V2-*_V3-*_w1-*_w2-*_w3-*_d1-*_d2-*.jpg"

# Get the list of image files
files = glob.glob(folder + "/" + pattern)
print(f"Found {len(files)} image files matching the pattern")

# Define the custom dtype
dtype = np.dtype([("V1", np.float64), ("V2", np.float64), ("V3", np.float64), ("w1", np.float64), ("w2", np.float64), ("w3", np.float64), ("d1", np.float64), ("d2", np.float64), ("contours", h5py.vlen_dtype(np.float64))])
# Create an empty structured array with the custom dtype
data = np.empty((0,), dtype=dtype)


# Create a HDF5 file named "contours.hdf5" in write mode
with h5py.File("contours.hdf5", "w") as f:
#     # Create a custom dtype that can store a variable number of floats
#     vlen_float = h5py.special_dtype(vlen=np.dtype('float64'))
#     # Create a dataset named "contours" with a variable length and dtype
#     dset = f.create_dataset("contours", shape=(0,), dtype=vlen_float)
    start_time = time.time()
    
    # Loop through the image files
    for i, file in enumerate(files):
        sys.stdout.write(f"\rProcessing image {i+1}/{len(files)}, time elapsed: {time.time() - start_time}")
        match = re.search("V1-([+-]?\\d+)_V2-([+-]?\\d+)_V3-([-+]?\\d+)_w1-(\\d+)_w2-(\\d+)_w3-(\\d+)_d1-(\\d+)_d2-(\\d+)", file)
        if match:
            V1 = match.group(1)
            V2 = match.group(2)
            V3 = match.group(3)
            w1 = match.group(4)
            w2 = match.group(5)
            w3 = match.group(6)
            d1 = match.group(7)
            d2 = match.group(8)
        # vars = [V1, V2, V3, w1, w2, w3, d1, d2]
        # vars = [float(v) for v in vars]
        vars = {'V1': int(V1), 'V2': int(V2), 'V3': int(V3), 'w1': int(w1), 'w2': int(w2), 'w3': int(w3), 'd1': int(d1), 'd2': int(d2)}
        contours, contours_area, contour_centroids, _ = droplet_boundary_detect.contour_finder(file)
        
        group = f.create_group(f"image_{i+1}")
        # Store the input variables as attributes of the group
        for var in vars:
            group.attrs[var] = vars[var]
        # Convert the contours to a NumPy array
        # contours = np.array(contours)
        # Flatten the contours array
        # contours = contours.flatten()
        # Resize the dataset to accommodate the new data
        # dset.resize(i + 1, axis=0)
        # Write the contours to the dataset
        # dset[i] = contours
        # row = np.array([(vars[0], vars[1], vars[2], vars[3], vars[4], vars[5], vars[6], vars[7], contours)], dtype=dtype)
        # Append the row to the data array
        # data = np.append(data, row)
        # Convert the contours to a NumPy array
        if len(contours) > 0:
            contour = contours[0][:,0,:]
            coeffs, a0, c0 = droplet_boundary_detect.contour_fourier_features(contour, 20)
            subdataset = group.create_dataset(f"contour_fourier_features", data=coeffs)#, name=f"contour_{i+1}"
            subdataset.attrs["a0"] = a0
            subdataset.attrs["c0"] = c0
        for j, contour in enumerate(contours):
            contour = np.array(contour)
            subdataset = group.create_dataset(f"contour_{j+1}", data=contour)#, name=f"contour_{i+1}"
            subdataset.attrs["area"] = contours_area[j]
            subdataset.attrs["centroid"] = contour_centroids[j]
            # print(c.shape)
            # c = c.flatten()
            # contours = np.append(contours, c)
            # print(c.shape)
            # if len(c) < 5:
            #     print(c)
        # contours = np.array(contours)
        # Create a new row with the input variables and the contours
        # row = np.array([(vars[0], vars[1], vars[2], vars[3], vars[4], vars[5], vars[6], vars[7], contours)], dtype=dtype)
        # Append the row to the data array
        # data = np.append(data, row)
        sys.stdout.flush()

# Create a HDF5 file and a dataset with the same dtype
# with h5py.File("data.hdf5", "w") as f:
    # dset = f.create_dataset("data", data=data, dtype=dtype)
        
sys.stdout.write(f"\n{len(files)} images processed in {time.time() - start_time} seconds.\n")

# How to read contours from HDF5 file
# with h5py.File("contours.hdf5", "r") as f:
#     # Loop through the groups
#     for i, group in enumerate(f.values()):
#         # Print the group name and attributes
#         print(group.name)
#         # print group attributes
#         for attr in group.attrs:
#             print(attr, group.attrs[attr])
#         # print(group.attrs.items())
#         # Loop through the subdatasets
#         for subdataset in group.values():
#             # Print the subdataset name and data
#             print(subdataset.name)
#             # print(subdataset[:])
            
#     for i, file in enumerate(files):
#         group = f[f"image_{i+1}"]
#         # Print the group name and attributes
#         print(group.name)
#         print(group.attrs.items())
#         # Loop through the subdatasets
#         for subdataset in group.values():
#             # Print the subdataset name and data
#             print(subdataset.name)
#             print(subdataset[:])
