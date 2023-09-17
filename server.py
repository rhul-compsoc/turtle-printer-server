import socket
import io
import os
import sys
from dotenv import load_dotenv
from PIL import Image
from escpos.printer import Usb

# Config
load_dotenv()
try:
    PORT = int(os.environ["SERVER_PORT"])
    USB_VENDOR_ID = int(os.environ["USB_VENDOR_ID"], 16)
    USB_PRODUCT_ID = int(os.environ["USB_PRODUCT_ID"], 16)
except KeyError as e:
    print(f"Missing config value {e}")
    sys.exit(1)
except ValueError:
    print(f"Config value must be an integer")
    sys.exit(1)

running = True

# Create server socket
# Continuously accept new connections
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    # Create receipt printer reference
    printer = Usb(USB_VENDOR_ID, USB_PRODUCT_ID, 0)

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
            # Print the image
            printer.image(io.BytesIO(img_bytes))
            # Cut the receipt
            printer.cut()
