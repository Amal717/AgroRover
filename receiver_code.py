import zmq

def subscribe_to_joystick_events():
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.connect("tcp://localhost:5555")  # Use the same address as in the publisher

    # Subscribe to all messages
    socket.setsockopt_string(zmq.SUBSCRIBE, '')

    while True:
        message = socket.recv_string()
        print("Received:", message)

if __name__ == "__main__":
    subscribe_to_joystick_events()
