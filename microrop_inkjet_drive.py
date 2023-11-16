import time
from PIL import Image

# Import your previously defined classes
from inkjet_dispenser import InkjetDispenser
from camera_controller import CameraController
# from image_processor import ImageProcessor
import droplet_boundary_detect as dbd

# Define the serial port and settings
port = '/dev/ttyUSB0'  # Replace with your serial port
baud_rate = 19200
# parity = serial.PARITY_NONE
# data_bits = 8
# stop_bits = 1

if __name__ == "__main__":
    try:
        # Initialize and turn on the inkjet dispenser
        dispenser = InkjetDispenser(port, baud_rate)
        dispenser.back_light(1, 50)  # Set backlight brightness
        dispenser.set_active(1, 1)   # Set the dispenser to active state
        dispenser.start_global(1)
        dispenser.back_light(1, 50)  # Set backlight brightness

        # Initialize and start the camera stream
        camera_controller = CameraController()
        camera_controller.initialize_camera()
        camera_controller.start_stream()

        # Capture an image
        image_path = "captured_image.jpg"
        camera_controller.capture_image(save_path=image_path)

        # Stop the camera stream
        camera_controller.stop_stream()

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
        dbd.droplet_boundary(image_path)

    except Exception as e:
        print(f"Error: {e}")

    # finally:
        # Close the camera
        # camera_controller.close_camera()
