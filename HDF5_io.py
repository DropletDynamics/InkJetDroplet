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
