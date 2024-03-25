import serial
import time

class InkjetDispenser:
    def __init__(self, port='COMx', baudrate=19200, timeout=1):
        self.ser = serial.Serial(port, baudrate, timeout=timeout)
        time.sleep(2)  # Allow time for the connection to establish

    def send_command(self, command):
        self.ser.write(command.encode() + b'\r')  # Add carriage return at the end
        response = self.ser.readline()
        # print(response)
        return response#.decode().strip()

    def back_light(self, head, brightness_percent):
        command = f"BackLight({head},{brightness_percent})"
        print("Setting backlight for head", head, "to", brightness_percent, "%")
        return self.send_command(command)

    def get_busy(self, head):
        command = f"GetBusy({head})"
        result = self.send_command(command)
        print("Getting busy status for head", head, " = ", (result))
        return result

    def get_config(self, head, n):
        command = f"GetConfig({head},{n})"
        result = float(self.send_command(command).decode())
        print("Getting config", n, "for head", head, " = ", result)
        return result

    def set_config(self, head, n, f):
        command = f"SetConfig({head},{n},{f})"
        print("Setting config", n, "for head", head, "to", f)
        return self.send_command(command)

    def get_drops(self, head):
        command = f"GetDrops({head})"
        result = int(self.send_command(command).decode())
        print("Getting drops for head", head, " = ", result)
        return self.send_command(command)

    def set_drops(self, head, n):
        command = f"SetDrops({head},{n})"
        print("Setting drops for head", head, "to", n)
        return self.send_command(command)
    
    def set_active(self, head, n):
        command = f"SetActive({head},{n})"
        print("Setting active for head", head, "to", n)
        return self.send_command(command)
    
    def start_global(self, n):
        command = f"StartGlobal({n})"
        print("Starting global action", n)
        return self.send_command(command)
    
    def get_frequency(self, head):
        command = f"GetFrequency({head})"
        result = float(self.send_command(command).decode().strip())
        print("Getting frequency for head", head, " = ", result)
        return result
    
    def set_frequency(self, head, frequency):
        command = f"SetFrequency({head},{frequency})"
        print(f"Setting frequency for head {head} to {frequency}")
        return self.send_command(command)
    
    def get_pulse_delay(self, head, pulse):
        command = f"GetPulseDelay({head},{pulse})"
        result = float(self.send_command(command).decode().strip()[1:])
        print(f"Getting pulse delay for head {head} pulse {pulse} = ", result)
        return result
    
    def set_pulse_delay(self, head, pulse, delay):
        command = f"SetPulseDelay({head},{pulse},{delay})"
        # print(f"Setting pulse delay for head {head} pulse {pulse} to {delay}")
        return self.send_command(command)
    
    def get_pulse_length(self, head, pulse):
        command = f"GetPulseLength({head},{pulse})"
        result = float(self.send_command(command).decode().strip()[1:])
        print(f"Getting pulse length for head {head} pulse {pulse} = ", result)
        return result
    
    def set_pulse_length(self, head, pulse, length):
        command = f"SetPulseLength({head},{pulse},{length})"
        # print(f"Setting pulse length for head {head} pulse {pulse} to {length}")
        return self.send_command(command)
    
    def get_pulse_voltage(self, head, pulse):
        command = f"GetPulseVoltage({head},{pulse})"
        result = float(self.send_command(command).decode().strip()[1:])
        print(f"Getting pulse voltage for head {head} pulse {pulse} = ", result)
        return result
    
    def set_pulse_voltage(self, head, pulse, voltage):
        command = f"SetPulseVoltage({head},{pulse},{voltage})"
        # print(f"Setting pulse voltage for head {head} pulse {pulse} to {voltage}")
        return self.send_command(command)
    
    def get_pulse_count(self, head):
        command = f"GetPulseCount({head})"
        response = self.send_command(command).decode().strip()
        if len(response)>1:
            result = int(response[1:])
        else:
            result = int(response)
        print(f"Getting pulse count for head {head} = ", result)
        return result
    
    def set_pulse_count(self, head, count):
        command = f"SetPulseCount({head},{count})"
        print(f"Setting pulse count for head {head} to {count}")
        return self.send_command(command)
    
    def refresh_pulse(self, head):
        command = f"RefreshPulse({head})"
        print(f"Refreshing pulse for head {head}")
        return self.send_command(command)
    
    def set_strobe_delay(self, head, delay):
        command = f"SetStrobe({head},{delay})"
        # print(f"Setting strobe delay for head {head} to {delay}")
        return self.send_command(command)
    
    def get_strobe_delay(self, head):
        command = f"GetStrobe({head})"
        result = float(self.send_command(command).decode().strip()[1:])
        print(f"Getting strobe delay for head {head} = ", result)
        return result
    
    def get_hardware_version(self):
        command = "GetConfig(1,3)"
        result = float(self.send_command(command).decode())
        print("Hardware vesion ", result)
        return result
    
    def get_software_version(self):
        command = "GetConfig(1,6)"
        result = (self.send_command(command).decode()).strip()
        print("Identification and software version ", result)
        return result
    
    
    
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