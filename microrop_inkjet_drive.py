import time
from PIL import Image

# Import your previously defined classes
from inkjet_dispenser import InkjetDispenser
from camera_controller import CameraController
# from image_processor import ImageProcessor
import droplet_boundary_detect as dbd
import add_metadata_to_image as mdi

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

        dispenser.set_pulse_voltage(1,1,-67.0)
        dispenser.set_pulse_voltage(1,2,52.0)
        dispenser.set_pulse_voltage(1,3,20.0)

        dispenser.set_pulse_length(1,1,10)
        dispenser.set_pulse_length(1,2,10)
        dispenser.set_pulse_length(1,3,5)

        dispenser.set_pulse_delay(1,1,5)
        dispenser.set_pulse_delay(1,2,5)
        dispenser.set_pulse_delay(1,3,9)

        dispenser.set_active(1, 1)   # Set the dispenser to active state
        dispenser.start_global(1)
        # dispenser.get_busy(1)

    


        print("Initialize and start the camera stream")
        camera_controller = CameraController()
        camera_controller.initialize_camera()
        camera_controller.start_stream()

        for V2 in range(40,60,2):
        # dispenser.set_pulse_voltage(1,1,-67.0)
            dispenser.set_pulse_voltage(1,2,V2)
        # dispenser.set_pulse_voltage(1,3,20.0)

        # dispenser.set_pulse_length(1,1,10)
        # dispenser.set_pulse_length(1,2,10)
        # dispenser.set_pulse_length(1,3,5)

        # dispenser.set_pulse_delay(1,1,5)
        # dispenser.set_pulse_delay(1,2,5)
        # dispenser.set_pulse_delay(1,3,9)
            for V3 in range(10,30,3):
                dispenser.set_pulse_voltage(1,3,V3)
                time.sleep(2)


        

        # # # Capture an image
                image_path = f"captured_image_V2-{V2}_V3-{V3}.jpg"
                numpy_image = camera_controller.capture_image()
                camera_controller.save_image(numpy_image=numpy_image, save_path=image_path)

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