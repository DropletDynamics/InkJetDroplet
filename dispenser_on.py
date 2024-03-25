from inkjet_dispenser import InkjetDispenser

# Define the serial port and settings
port = '/dev/ttyUSB0'  # Replace with your serial port
baud_rate = 19200
# parity = serial.PARITY_NONE
# data_bits = 8
# stop_bits = 1

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

        dispenser.set_active(1, 1)   # Set the dispenser to active state
        dispenser.start_global(1)
        # dispenser.set_active(1, 0)   # Set the dispenser to active state
        # dispenser.get_busy(1)

        # dispenser.start_global(0)
        # dispenser.close()

    except Exception as e:
        print(f"Error: {e}")
