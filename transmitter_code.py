import zmq
from inputs import devices, get_gamepad

button_mapping = {
    'BTN_WEST': 'Y',
    'BTN_NORTH': 'X',
    'BTN_SOUTH': 'A',
    'BTN_EAST': 'B',
    'BTN_SELECT': 'SELECT',
    'BTN_START': 'START',
    'BTN_MODE': 'HOME',
    'BTN_TL': 'L1',
    'BTN_TR': 'R1'
}

axis_mapping = {
    'ABS_X': 'LJ_X-axis',
    'ABS_Y': 'LJ_Y-axis',
    'ABS_Z': 'RJ_X-axis',
    'ABS_RZ': 'RJ_Y-axis',
    'ABS_BRAKE': 'L2',
    'ABS_GAS': 'R2'
}

hat_mapping = {
    'ABS_HAT0Y': {
        -1: 'UP',
        1: 'DOWN'
    },
    'ABS_HAT0X': {
        -1: 'LEFT',
        1: 'RIGHT'
    }
}

def send_joystick_event(context, event):
    socket = context.socket(zmq.PUB)
    socket.bind("tcp://127.0.0.1:5555")  # Change the address as needed

    # Process joystick event
    if event.ev_type == 'Key':
        button = button_mapping.get(event.code)
        if button:
            message = f"Button {button}: State {event.state}"
            print(message)  # Print the joystick message
            socket.send_string(message)
    elif event.ev_type == 'Absolute':
        axis = axis_mapping.get(event.code)
        if axis:
            if isinstance(axis, dict):
                for key in axis:
                    if isinstance(key, range) and event.state in key:
                        value = axis[key]
                        if value is not None:
                            message = f"Axis {value}: Value {event.state}"
                            print(message)  # Print the joystick message
                            socket.send_string(message)
                            break
            else:
                message = f"Axis {axis}: Value {event.state}"
                print(message)  # Print the joystick message
                socket.send_string(message)
        elif event.code in hat_mapping:
            hat_value = hat_mapping[event.code].get(event.state)
            if hat_value:
                message = f"Hat {hat_value}"
                print(message)  # Print the joystick message
                socket.send_string(message)

# Get gamepad devices
gamepad_devices = devices.gamepads
if not gamepad_devices:
    print("No gamepad devices found.")
    exit()

# Select the first gamepad device
gamepad = gamepad_devices[0]

# Set up ZeroMQ context
context = zmq.Context()

# Main loop to read joystick input and publish messages
while True:
    events = get_gamepad()
    for event in events:
        if event.device == gamepad:
            send_joystick_event(context, event)
