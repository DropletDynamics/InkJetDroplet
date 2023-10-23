import cv2
import numpy as np
from PIL import Image

class ImageProcessor:
    def __init__(self):
        pass

    def load_image(self, image_path):
        # Load the image using Pillow
        return Image.open(image_path)

    def preprocess_image(self, image):
        # Convert the image to a format suitable for OpenCV
        return np.array(image)

    def detect_droplet_boundary(self, image_path):
        # Load the image
        original_image = self.load_image(image_path)

        # Preprocess the image for OpenCV
        cv_image = self.preprocess_image(original_image)

        # Convert the image to grayscale
        gray_image = cv2.cvtColor(cv_image, cv2.COLOR_RGB2GRAY)

        # Apply thresholding to segment the droplet
        _, binary_image = cv2.threshold(gray_image, 200, 255, cv2.THRESH_BINARY)

        # Find contours in the binary image
        contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Draw the contours on the original image
        result_image = cv_image.copy()
        cv2.drawContours(result_image, contours, -1, (0, 255, 0), 2)

        # Convert the result image back to Pillow format for display
        result_image_pil = Image.fromarray(result_image)

        # Display the result image
        result_image_pil.show()

        return result_image_pil

# Example usage
# if __name__ == "__main__":
#     image_processor = ImageProcessor()

#     # Replace 'your_image_path.jpg' with the path to the image captured by the camera
#     processed_image = image_processor.detect_droplet_boundary('your_image_path.jpg')

