import socket
import io
import os
import sys
from dotenv import load_dotenv
from PIL import Image

# Config
load_dotenv()
try:
    PORT = int(os.environ["SERVER_PORT"])
except KeyError as e:
    print(f"Missing config value {e}")
    sys.exit(1)
except ValueError:
    print("Config value SERVER_PORT must be an integer")
    sys.exit(1)

running = True

# Create server socket
# Continuously accept new connections
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.bind(("", PORT))
    sock.listen()
    # Accept incoming connections
    while running:
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