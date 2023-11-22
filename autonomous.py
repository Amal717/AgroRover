import csv
import time
import serial

ser = serial.Serial('COMX', 9600, timeout=1)  # Replace 'COMX' with the correct serial port

csv_filename = "joystick_commands.csv"

# Example content of joystick_commands.csv:
# 1637716800.0,BUTTON_A
# 1637716810.0,BUTTON_B
# 1637716820.0,AXIS_X:0.5

def send_commands_from_csv(ser, csv_filename):
    with open(csv_filename, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            timestamp, command = row
            current_time = time.time()

            # Wait until the specified timestamp is reached
            while current_time < float(timestamp):
                current_time = time.time()
                time.sleep(0.1)  # Adjust sleep duration as needed

            # Send the joystick command to Arduino
            ser.write(command.encode())
            print(f"Sent Joystick Command to Arduino: {command}")

# Run the function to send commands from the CSV file
send_commands_from_csv(ser, csv_filename)

# Close the serial port when done
ser.close()
