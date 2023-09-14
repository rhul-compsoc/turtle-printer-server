import socket

# Config
PORT = 4444

running = True

# Create server socket
while running:
    # Continuously accept new connections
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("localhost", PORT))
        sock.listen()
        # Accept incoming connections
        conn, addr = sock.accept()
        with conn:
            print(f"New connection from {addr}")
            # Receive image size
            n_bytes = conn.recv(4)
            print(f"Image size: {int.from_bytes(n_bytes, 'big')}")