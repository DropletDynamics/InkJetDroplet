import time
from PIL import Image

from inkjet_dispenser import InkjetDispenser
from camera_controller import CameraController
# from image_processor import ImageProcessor
import droplet_boundary_detect as dbd
import add_metadata_to_image as mdi
import HDF5_io
import cv2
# Import the pickle module
# import pickle
import sys
from pathlib import Path
import os


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
        dispenser.get_strobe_delay(1)

        # Define the initial values of the loop variables
        V1_init = -98
        V2_init = 12
        V3_init = 0
        w1_init = 20
        w2_init = 10
        w3_init = 1
        d1_init = 5
        d2_init = 5

        # dispenser.set_pulse_voltage(1,1,V1_init)
        # dispenser.set_pulse_voltage(1,2,V2_init)
        # dispenser.set_pulse_voltage(1,3,V3_init)

        # dispenser.set_pulse_length(1,1,w1_init)
        # dispenser.set_pulse_length(1,2,w2_init)
        # dispenser.set_pulse_length(1,3,w3_init)

        # dispenser.set_pulse_delay(1,1,d1_init)
        # dispenser.set_pulse_delay(1,2,d2_init)
        # dispenser.set_pulse_delay(1,3,9)

        dispenser.set_active(1, 1)   # Set the dispenser to active state
        dispenser.start_global(1)
        # # dispenser.get_busy(1)

    


        print("Initialize and start the camera stream")
        camera_controller = CameraController()
        camera_controller.initialize_camera()
        camera_controller.start_stream()
        width = camera_controller.width
        height = camera_controller.height

        fps = 30
        out = cv2.VideoWriter(f"V1-{V1_init}_V2-{V2_init}_V3-{V3_init}_w1-{w1_init}_w2-{w2_init}_w3-{w3_init}_d1-{d1_init}_d2-{d2_init}.mkv", cv2.VideoWriter_fourcc(*'RGBA'), fps, (width, height), False)

        # hdf_file = HDF5_io.HDF5ImageSaver('numpy_images.hdf5')

        

        
        image_path = f"videos/V1-{V1_init}_V2-{V2_init}_V3-{V3_init}_w1-{w1_init}_w2-{w2_init}_w3-{w3_init}_d1-{d1_init}_d2-{d2_init}"
        path = Path(image_path)
        if not path.exists():
            path.mkdir(parents=True, exist_ok=True)
        
        
        # # Use a try-except-finally block to handle interruptions
        try:         
            

            for strobe in range(0,1000):
                sys.stdout.write(f"Strobe delay = {strobe}\r")
                dispenser.set_strobe_delay(1,strobe)                
                time.sleep(0.1)
                image_file = image_path + '/image_{}.jpg'.format(str(strobe).zfill(4))
                numpy_image = camera_controller.capture_image()
                out.write(numpy_image)
                camera_controller.save_image(numpy_image=numpy_image, save_path=image_file)
                sys.stdout.flush()

            out.release()
           
        except Exception as e:
            # If an exception occurs, print the error message and exit
            print(f"An error occurred: {e}")
            exit()

        # # finally:
        # #     # If the process is interrupted, delete the progress file
        # #     if os.path.exists(progress_file):
        # #     os.remove(progress_file)


        # # 
        # # 

        # # 
        # # 
        # # dispenser.set_pulse_delay(1,3,9)
                
                    

        # # # # # Stop the camera stream
        # camera_controller.stop_stream()

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