import gxipy as gx
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 

class CameraController:
    def __init__(self):
        self.device_manager = gx.DeviceManager()
        self.camera = None

    def initialize_camera(self):
        dev_num, dev_info_list = self.device_manager.update_device_list()
        if dev_num == 0:
            raise Exception("No camera found.")

        # Open the first available camera
        strSN = dev_info_list[0].get("sn")
        self.camera = self.device_manager.open_device_by_sn(strSN)
        int_channel_num = self.camera.get_stream_channel_num()
        print("Camera chanells = ",int_channel_num)
        self.width = self.camera.Width.get()
        self.height = self.camera.Height.get()
        print("Image size = ", self.width, self.height)

    def start_stream(self):
        if self.camera is None:
            raise Exception("Camera not initialized.")

        self.camera.stream_on()
        print("CameraGain = ",self.camera.Gain.get(), self.camera.Gain.get_range())
        self.camera.Gain.set(12)

    def capture_image(self):
        if self.camera is None:
            raise Exception("Camera not initialized.")

        raw_image = self.camera.data_stream[0].get_image()
        # print(raw_image)
        rgb_image = raw_image.convert("RGB")

        if rgb_image is not None:
            numpy_image = rgb_image.get_numpy_array()
            return numpy_image
            # if numpy_image is not None:
            #     image = Image.fromarray(numpy_image, 'RGB')
            #     image.show()
            #     image.save(save_path)
        else: return None

    def save_image(self, numpy_image, save_path="image.jpg", add_timestamp=False, timestamp=''):
        if numpy_image is not None:
            image = Image.fromarray(numpy_image, 'RGB')
            # image.show()
            if add_timestamp:
                draw = ImageDraw.Draw(image)
                # font = ImageFont.truetype(<font-file>, <font-size>)
                font = ImageFont.truetype("sans-serif.ttf", 16)
                # draw.text((x, y),"Sample Text",(r,g,b))
                draw.text((10, 10),timestamp,(255,255,255),font=font)
            image.save(save_path)

    def stop_stream(self):
        if self.camera is not None:
            self.camera.stream_off()

    def close_camera(self):
        if self.camera is not None:
            self.camera.close_device()

# Example usage
# if __name__ == "__main__":
#     camera_controller = CameraController()

#     try:
#         camera_controller.initialize_camera()
#         camera_controller.start_stream()

#         # Capture an image and save it
#         camera_controller.capture_image()

#     finally:
#         # Make sure to stop the stream and close the camera
#         camera_controller.stop_stream()
#         camera_controller.close_camera()

