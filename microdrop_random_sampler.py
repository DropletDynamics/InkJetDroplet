import time
from PIL import Image

from inkjet_dispenser import InkjetDispenser
from camera_controller import CameraController
# from image_processor import ImageProcessor
import droplet_boundary_detect as dbd
import add_metadata_to_image as mdi
import HDF5_io
import numpy as np
# Import the pickle module
import pickle
import sys

# Define a file name to store the progress
progress_file = "progress.pkl"

# Define a function to save the progress to the file
def save_progress(V1, V2, V3, w1, w2, w3, d1, d2):
    with open(progress_file, "wb") as f:
        pickle.dump((V1, V2, V3, w1, w2, w3, d1, d2), f)

# Define a function to load the progress from the file
def load_progress():
    with open(progress_file, "rb") as f:
        return pickle.load(f)

# Define the serial port and settings
port = '/dev/ttyUSB0'  # Replace with your serial port
baud_rate = 19200
# parity = serial.PARITY_NONE
# data_bits = 8
# stop_bits = 1

def initial_setup():
    print("Initialize and turn on the inkjet dispenser")
    dispenser = InkjetDispenser(port, baud_rate)
    
    dispenser.get_hardware_version()
    dispenser.get_software_version()
    
    dispenser.set_active(1, 1)   # Set the dispenser to active state
    dispenser.start_global(1)
    dispenser.back_light(1, 0.7)  # Set backlight brightness
    

    print("Initialize and start the camera stream")
    camera_controller = CameraController()
    camera_controller.initialize_camera()
    camera_controller.start_stream()



if __name__ == "__main__":
    try:
        
        print("Initialize and turn on the inkjet dispenser")
        dispenser = InkjetDispenser(port, baud_rate)
    
        dispenser.get_hardware_version()
        dispenser.get_software_version()
    
        # dispenser.get_busy(1)
        # dispenser.refresh_pulse(1)
        n_pulse = dispenser.get_pulse_count(1)
        for i in range(1,n_pulse+1):
            dispenser.get_pulse_voltage(1,i)
            dispenser.get_pulse_delay(1,i)
            dispenser.get_pulse_length(1,i)
        dispenser.back_light(1, 30)  # Set backlight brightness
        dispenser.set_strobe_delay(1,200)

        # dispenser.set_pulse_voltage(1,1,-95.0)
        # dispenser.set_pulse_voltage(1,2,12.0)
        # dispenser.set_pulse_voltage(1,3,-95)

        # dispenser.set_pulse_length(1,1,33)
        # dispenser.set_pulse_length(1,2,15)
        # dispenser.set_pulse_length(1,3,33)

        # dispenser.set_pulse_delay(1,1,8)
        # dispenser.set_pulse_delay(1,2,7)
        # dispenser.set_pulse_delay(1,3,9)

        dispenser.set_active(1, 1)   # Set the dispenser to active state
        dispenser.start_global(1)
        # dispenser.get_busy(1)

    


        print("Initialize and start the camera stream")
        camera_controller = CameraController()
        camera_controller.initialize_camera()
        camera_controller.start_stream()
        width = camera_controller.width
        height = camera_controller.height

        # hdf_file = HDF5_io.HDF5ImageSaver('numpy_images.hdf5')

        number_of_images = 200000

        # Define the ranges of input variables
        V1_min = -120
        V2_min = 10
        V3_min = -40
        w1_min = 5
        w2_min = 5
        w3_min = 1
        d1_min = 0
        d2_min = 0

        V1_max = -50
        V2_max = 50
        V3_max = 40
        w1_max = 40
        w2_max = 40
        w3_max = 40
        d1_max = 20
        d2_max = 20

        V1 = np.random.randint(V1_min, V1_max, number_of_images)
        V2 = np.random.randint(V2_min, V2_max, number_of_images)
        V3 = np.random.randint(V3_min, V3_max, number_of_images)
        w1 = np.random.randint(w1_min, w1_max, number_of_images)
        w2 = np.random.randint(w2_min, w2_max, number_of_images)
        w3 = np.random.randint(w3_min, w3_max, number_of_images)
        d1 = np.random.randint(d1_min, d1_max, number_of_images)
        d2 = np.random.randint(d2_min, d2_max, number_of_images)

        # # Try to load the progress from the file, if it exists
        # try:
        #     V1, V2, V3, w1, w2, w3, d1, d2 = load_progress()
        # except FileNotFoundError:
        #     # If the file does not exist, use the initial values
        #     V1, V2, V3, w1, w2, w3, d1, d2 = V1_init, V2_init, V3_init, w1_init, w2_init, w3_init, d1_init, d2_init

        # Use a try-except-finally block to handle interruptions
        try:
            # Loop through the parameters
            for i in range(number_of_images):
                dispenser.set_pulse_voltage(1,1,V1[i])
                dispenser.set_pulse_voltage(1,2,V2[i])                
                dispenser.set_pulse_voltage(1,3,V3[i])
                dispenser.set_pulse_length(1,1,w1[i])
                dispenser.set_pulse_length(1,2,w2[i])
                dispenser.set_pulse_length(1,3,w3[i])
                dispenser.set_pulse_delay(1,1,d1[i])
                dispenser.set_pulse_delay(1,2,d2[i])
                time.sleep(2)
                # group = hdf_file.create_group(f"image_{i}")
                # input_parameters = {'V1':V1[i], 'V2':V2[i], 'V3':V3[i], 'w1':w1[i], 'w2':w2[i], 'w3':w3[i], 'd1':d1[i], 'd2':d2[i]}
                # hdf_file.add_attributes(group, input_parameters)
                # # # Capture an image
                image_path = f"captures/images_V1-{V1[i]}_V2-{V2[i]}_V3-{V3[i]}_w1-{w1[i]}_w2-{w2[i]}_w3-{w3[i]}_d1-{d1[i]}_d2-{d2[i]}.jpg"
                numpy_image = camera_controller.capture_image()
                # group.create_dataset(f'numpy_image_{i}', data=numpy_image , compression="gzip", compression_opts=9)
                camera_controller.save_image(numpy_image=numpy_image, save_path=image_path)
                # Save the progress after each image
                # save_progress(V1, V2, V3, w1, w2, w3, d1, d2)
                sys.stdout.write(f"image_{i}: V1={V1[i]}, V2={V2[i]}, V3={V3[i]}, w1={w1[i]}, w2={w2[i]}, w3={w3[i]}, d1={d1[i]}, d2={d2[i]}\r")
                sys.stdout.flush()
        except Exception as e:
            # If an exception occurs, print the error message and exit
            print(f"An error occurred: {e}")
            exit()

        # finally:
        #     # If the process is interrupted, delete the progress file
        #     if os.path.exists(progress_file):
        #     os.remove(progress_file)


        # 
        # 

        # 
        # 
        # dispenser.set_pulse_delay(1,3,9)
                
                    

        # # # # Stop the camera stream
        camera_controller.stop_stream()

        # # Add metadata to the captured image
        # input_signal_properties = {"V1": 50, "V2": -60, "V3": 10, "w1": 27, "w2": 25, "w3": 26, "d1": 10, "d2": 20}
        # mdi.add_metadata_tags(image_path, input_signal_properties)

        # Close the inkjet dispenser
        # dispenser.set_active(1, 0)   # Set the dispenser to inactive state
        dispenser.start_global(0)
        dispenser.close()

        # Process the captured image to detect the droplet boundary
        # image_processor = ImageProcessor()
        # processed_image = image_processor.detect_droplet_boundary(image_path)

        # # Save the processed image
        # processed_image.save("processed_image.jpg")

        # Detect the droplet boundary from the captured image
        # ellipses = dbd.droplet_boundary(image_path)

    except Exception as e:
        print(f"Error: {e}")

    # finally:
        # Close the camera
        # camera_controller.close_camera()