import time
from PIL import Image

# Import your previously defined classes
from inkjet_dispenser import InkjetDispenser
from camera_controller import CameraController
# from image_processor import ImageProcessor
import droplet_boundary_detect as dbd
import add_metadata_to_image as mdi
import HDF5_io

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
        # dispenser.get_strobe_delay(1)

        dispenser.set_pulse_voltage(1,1,-95.0)
        dispenser.set_pulse_voltage(1,2,12.0)
        dispenser.set_pulse_voltage(1,3,-95)

        dispenser.set_pulse_length(1,1,33)
        dispenser.set_pulse_length(1,2,15)
        dispenser.set_pulse_length(1,3,33)

        dispenser.set_pulse_delay(1,1,8)
        dispenser.set_pulse_delay(1,2,7)
        dispenser.set_pulse_delay(1,3,9)

        dispenser.set_active(1, 1)   # Set the dispenser to active state
        dispenser.start_global(1)
        # dispenser.get_busy(1)

    


        print("Initialize and start the camera stream")
        camera_controller = CameraController()
        camera_controller.initialize_camera()
        camera_controller.start_stream()
        width = camera_controller.width
        height = camera_controller.height

        hdf_file = HDF5_io.HDF5ImageSaver('numpy_images.hdf5')

        # Define the initial values of the loop variables
        V1_init = -98
        V2_init = 12
        V3_init = 0
        w1_init = 20
        w2_init = 10
        w3_init = 1
        d1_init = 5
        d2_init = 5

        # Try to load the progress from the file, if it exists
        try:
            V1, V2, V3, w1, w2, w3, d1, d2 = load_progress()
        except FileNotFoundError:
            # If the file does not exist, use the initial values
            V1, V2, V3, w1, w2, w3, d1, d2 = V1_init, V2_init, V3_init, w1_init, w2_init, w3_init, d1_init, d2_init

        # Use a try-except-finally block to handle interruptions
        try:
            # Loop through the parameters
            for V1 in range(V1,-70,4):
                dispenser.set_pulse_voltage(1,1,V1)
                for V2 in range(V2,15):
                    dispenser.set_pulse_voltage(1,2,V2)
                    for V3 in range(V3,-35,-5):
                        group = hdf_file.create_group(f"images_V1-{V1}_V2-{V2}_V3-{V3}")
                        dispenser.set_pulse_voltage(1,3,V3)
                        # if (V1==-98 and V2==12 and V3==0):
                        #     w1_min = 23
                        # else:
                        #     w1_min = 20
                        for w1 in range(w1,36,3):
                            dispenser.set_pulse_length(1,1,w1)
                            for w2 in range(w2,16):
                                dispenser.set_pulse_length(1,2,w2)
                                for w3 in range(w3,33,3):
                                    dispenser.set_pulse_length(1,3,w3)
                                    for d1 in range(d1,8):
                                        dispenser.set_pulse_delay(1,1,d1)
                                        for d2 in range(d2,8):
                                            dispenser.set_pulse_delay(1,2,d2)
                                            time.sleep(2)
                                            # # # Capture an image
                                            image_path = f"captures/images_V1-{V1}_V2-{V2}_V3-{V3}_w1-{w1}_w2-{w2}_w3-{w3}_d1-{d1}_d2-{d2}.jpg"
                                            numpy_image = camera_controller.capture_image()
                                            camera_controller.save_image(numpy_image=numpy_image, save_path=image_path)
                                            # Save the progress after each image
                                            save_progress(V1, V2, V3, w1, w2, w3, d1, d2)
                                            sys.stdout.write(f"V1={V1}, V2={V2}, V3={V3}, w1={w1}, w2={w2}, w3={w3}, d1={d1}, d2={d2}\r")
                                            sys.stdout.flush()
                                        # Reset d2 for the next iteration
                                        d2 = d2_init
                                    # Reset w3 and d1 for the next iteration
                                    d1 = d1_init
                                w3 = w3_init
                            # Reset w2 for the next iteration
                            w2 = w2_init
                        # Reset w1 for the next iteration
                        w1 = w1_init
                    # Reset V3 for the next iteration
                    V3 = V3_init
                # Reset V2 for the next iteration
                V2 = V2_init
            # Reset V1 for the next iteration
            V1 = V1_init
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