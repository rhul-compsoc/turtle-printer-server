import socket
import io
from PIL import Image

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
            n_bytes = int.from_bytes(conn.recv(4), "big")
            # Now receive whole image
            img_bytes = conn.recv(n_bytes)
            # Open the image
            img = Image.open(io.BytesIO(img_bytes))
            img.save("received.png")