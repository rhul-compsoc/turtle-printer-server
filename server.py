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

# resize_image resizes the image to satisfy the given min_width and max_height parameters
def resize_image(img, min_width, max_height):
    # Resize image uniformly
    fact = min_width / img.width
    height = int(img.height * fact)
    # Clamp height
    clamped_height = min(height, max_height)
    fact = clamped_height / height
    width = int(min_width * fact)
    return img.resize((width, clamped_height))

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
            img = Image.open(io.BytesIO(img_bytes))
            # Resize the image
            img = resize_image(img, 450, 750)
            # Print the image
            printer.image(img)
            # Add QR code for linktree
            printer.text("\n" * 2)
            printer.qr("http://links.cmpsc.uk", size=8)
            # Cut the receipt
            printer.cut()


