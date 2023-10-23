import serial
import time

class InkjetDispenser:
    def __init__(self, port='COMx', baudrate=19200, timeout=1):
        self.ser = serial.Serial(port, baudrate, timeout=timeout)
        time.sleep(2)  # Allow time for the connection to establish

    def send_command(self, command):
        self.ser.write(command.encode() + b'\r')  # Add carriage return at the end
        response = self.ser.readline().decode().strip()
        return response

    def back_light(self, head, brightness_percent):
        command = f"BackLight({head},{brightness_percent})"
        return self.send_command(command)

    def get_busy(self, head):
        command = f"GetBusy({head})"
        return self.send_command(command)

    def get_config(self, head, n):
        command = f"GetConfig({head},{n})"
        return self.send_command(command)

    def set_config(self, head, n, f):
        command = f"SetConfig({head},{n},{f})"
        return self.send_command(command)

    def get_drops(self, head):
        command = f"GetDrops({head})"
        return self.send_command(command)

    def set_drops(self, head, n):
        command = f"SetDrops({head},{n})"
        return self.send_command(command)
    
    def set_active(self, head, n):
        command = f"SetActive({head},{n})"
        return self.send_command(command)
    
    def start_global(self, n):
        command = f"StartGlobal({n})"
        return self.send_command(command)

    # Add more methods for other commands as needed...

    def close(self):
        self.ser.close()

# Example usage
# if __name__ == "__main__":
#     dispenser = InkjetDispenser(port='COMx', baudrate=19200)

#     try:
#         # Example command: BackLight(head, brightness percent)
#         response = dispenser.back_light(1, 50)
#         print("Response:", response)

#         # Example command: GetBusy(head)
#         response = dispenser.get_busy(1)
#         print("Response:", response)

#         # Example command: GetConfig(head, n)
#         response = dispenser.get_config(1, 2)
#         print("Response:", response)

#         # You can add more commands as needed...

#     finally:
#         dispenser.close()
