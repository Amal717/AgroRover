import zmq
import serial
import csv
import time
import os

context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("tcp://127.0.0.1:5555")
socket.setsockopt_string(zmq.SUBSCRIBE, '')

ser = serial.Serial('COMX', 9600, timeout=1)  # Replace 'COMX' with the correct serial port

# Generate a unique filename with a timestamp
timestamp = time.strftime("%Y%m%d%H%M%S")
csv_filename = f"received_data_{timestamp}.csv"

def create_csv_file(csv_filename):
    with open(csv_filename, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['Time', 'Joystick Cmd', 'Arduino Data'])

# Check if the file exists, if not create it with headers
if not os.path.isfile(csv_filename):
    create_csv_file(csv_filename)

def receive_and_store_data(context, ser, csv_writer):
    current_time = time.time()

    # Receive joystick command
    message = socket.recv_string()
    print(f"Received Joystick Input: {message}")

    # Send the received command to Arduino via serial
    ser.write(message.encode())

    # Receive response from Arduino via serial
    response = ser.readline().decode().strip()
    print(f"Response from Arduino: {response}")

    # Write data to CSV file
    csv_writer.writerow([current_time, message, response if response else '-1'])

# Main loop to continuously receive and process data
while True:
    try:
        with open(csv_filename, 'a', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            receive_and_store_data(context, ser, csv_writer)
    except KeyboardInterrupt:
        print("Exiting...")
        break

# Close the serial port when done
ser.close()
