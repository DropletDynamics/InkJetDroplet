import h5py
import numpy as np

def create_database(file_name):
    # Create a file object that represents the HDF5 file
    file = h5py.File(file_name, 'w')
    # Create a group object that represents the input parameters group
    group = file.create_group('input_parameters')

def create_and_store_data(file_name, input_parameters, output_parameters):
    # Create a file object that represents the HDF5 file
    file = h5py.File(file_name, 'w')
    
    # Create a group object that represents the input parameters group
    group = file.create_group('input_parameters')
    
    # Create datasets for each input parameter and store the data
    for key, value in input_parameters.items():
        dataset = group.create_dataset(key, data=value)
    
    # Define a custom data type for the output parameters
    dtype = np.dtype([('a1', 'f8'), ('a2', 'f8'), ('theta', 'f8')])
    
    # Convert the output parameters to a numpy array with the custom data type
    data = np.array(output_parameters, dtype=dtype)
    
    # Create a dataset for the output parameters and store the data
    dataset = file.create_dataset('output_parameters', data=data)
    
    # Close the file
    file.close()
    
class HDF5ImageSaver:
    def __init__(self, file_name):
        # Create a file object that represents the HDF5 file
        self.file = h5py.File(file_name, 'w')
    
    def create_group(self, group_name):
        # Create a group object that represents a group in the HDF5 file
        group = self.file.create_group(group_name)
        return group 

    def add_attributes(self, group, attributes):
        # Add attributes to the group object as metadata
        for key, value in attributes.items():
            group.attrs[key] = value
    
    def image_dataset(self, group, dataset_name, w, h):
        # Create a dataset with an initial shape of (0, 100, 100) and a maximum shape of (None, 100, 100)
        dataset = group.create_dataset(dataset_name, shape=(0, w, h), maxshape=(None, w, h), compression="gzip", compression_opts=9)
        return dataset
    
    def append_image(self, dataset, image_data):
        # Resize the dataset to increase the size along the first axis
        dataset.resize(dataset.shape[0] + 1, axis=0)

        # Assign the image data to the last position of the array
        dataset[-1, :, :] = image_data
    
    def close_file(self):
        # Close the file object
        self.file.close()
