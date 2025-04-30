import os
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageSequence, ExifTags
from stegano import lsb
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import cv2

# Initialize global variables
file_path = ""

def upload_file():
    global file_path, img_label
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpeg *.jpg *.png *.gif")])
    if file_path:
        label.config(text=f"File selected: {file_path}", bootstyle="success")
        img = Image.open(file_path)
        img.thumbnail((400, 400))
        img = ImageTk.PhotoImage(img)
        img_label.config(image=None)  # Clear the previous image
        img_label.config(image=img)
        img_label.image = img

        process_file(file_path)  

def upload_directory():
    directory_path = filedialog.askdirectory()
    if directory_path:
        label.config(text=f"Directory selected: {directory_path}", bootstyle="success")
        process_directory(directory_path)

def embed_message():
    if not file_path:
        analysis_label.config(text="Please upload a file first.", bootstyle="danger")
        return
    message = message_entry.get()
    if not message:
        analysis_label.config(text="Please enter a message to hide.", bootstyle="danger")
        return
    try:
        pass  # Placeholder for the intended code
        if not file_path.lower().endswith((".jpeg", ".jpg", ".png")):
            analysis_label.config(text="Unsupported file format. Please use JPEG or PNG.", bootstyle="danger")
            return
        output_path = file_path.rsplit('.', 1)[0] + "_stego.png"
        lsb.hide(file_path, message).save(output_path)
        truncated_output_path = (output_path[:50] + '...') if len(output_path) > 50 else output_path
        analysis_label.config(text=f"Hidden message embedded. Saved to: {truncated_output_path}", bootstyle="success")
    except Exception as e:
        analysis_label.config(text=f"Error embedding message: {e}", bootstyle="danger")

def reveal_message():
    try:
        hidden_message = lsb.reveal(file_path)
        if hidden_message:
            print(f"Hidden Message in {file_path}: {hidden_message}")
            truncated_message = (hidden_message[:50] + '...') if len(hidden_message) > 50 else hidden_message
            analysis_label.config(text=f"Hidden Message: {truncated_message}", bootstyle="success")
        else:
            print(f"No hidden message found in {file_path}.")
            analysis_label.config(text="No hidden message found.", bootstyle="warning")
    except ValueError as ve:
        print(f"File is not a valid image or does not contain a hidden message: {ve}")
        analysis_label.config(text="Invalid image or no hidden message found.", bootstyle="danger")
    except Exception as e:
        print(f"Error revealing hidden message: {e}")
        analysis_label.config(text=f"Error revealing message: {e}", bootstyle="danger")
        print(f"No hidden message found in {file_path}.")
        analysis_label.config(text="No hidden message found.", bootstyle="warning")
    except Exception as e:
        print(f"Error revealing hidden message: {e}")
        analysis_label.config(text=f"Error revealing message: {e}", bootstyle="danger")

def process_directory(directory_path):
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.lower().endswith((".jpg", ".jpeg", ".png", ".gif")):
                process_file(os.path.join(root, file))

def process_file(path):
    try:
        # Try LSB extraction
        try:
            hidden_message = lsb.reveal(path)
            if hidden_message:
                print(f"Hidden Message in {path}: {hidden_message}")
            else:
                print(f"No hidden message found in {path}.")
        except Exception as e:
            pass  # Placeholder to handle the exception
        try:
            exif_data = img._getexif()
            pass  # Placeholder for handling EXIF data
            if exif_data:
                print(f"\nEXIF Metadata for {path}:")
                for tag, value in exif_data.items():
                    tag_name = ExifTags.TAGS.get(tag, tag)
                    print(f"{tag_name:25}: {value}")
            else:
                print(f"No EXIF metadata found for {path}.")
        except Exception as e:
            pass  # Placeholder to handle the exception
        # Last 100 bytes of binary
        try:
            with open(path, 'rb') as f:
                data = f.read()
            if len(data) >= 100:
                print(f"\nLast 100 bytes of {path}:\n{data[-100:]}")
            else:
                print(f"\nFile {path} is smaller than 100 bytes. Full content:\n{data}")
        except Exception as e:
            print(f"Error reading binary from {path}: {e}")
        except Exception as e:
            print(f"Error reading binary from {path}: {e}")
            img = cv2.imread(path)
            if img is None:
                print(f"Could not read image {path} with OpenCV.")
            else:
                try:
                    print(f"\nImage Dimensions for {path}: {img.shape}")
                except Exception as e:
                    print(f"Error accessing image dimensions for {path}: {e}")
                print(f"\nImage Dimensions for {path}: {img.shape}")
                print(f"Could not read image {path} with OpenCV.")
        except Exception as e:
            print(f"Error analyzing pixel data from {path}: {e}")

    except Exception as e:
        print(f"Failed to process {path}: {e}")

# GUI Setup
window = ttk.Window(themename="superhero")
window.title("Python Steganography & Analysis Tool")
window.geometry("800x700")

upload_file_button = ttk.Button(window, text="Upload Single File", command=upload_file, bootstyle="primary")
upload_file_button.pack(pady=10)

upload_dir_button = ttk.Button(window, text="Upload Directory", command=upload_directory, bootstyle="warning")
upload_dir_button.pack(pady=10)

label = ttk.Label(window, text="No file or directory selected", bootstyle="danger")
label.pack(pady=10)

img_label = ttk.Label(window)
img_label.pack(pady=10)

message_label = ttk.Label(window, text="Enter the message to hide:", bootstyle="info")
message_label.pack(pady=5)

message_entry = ttk.Entry(window, width=35)
message_entry.pack(pady=5)

embed_button = ttk.Button(window, text="Embed Message", command=embed_message, bootstyle="success")
embed_button.pack(pady=10)

reveal_button = ttk.Button(window, text="Reveal Hidden Message", command=reveal_message, bootstyle="secondary")
reveal_button.pack(pady=10)

analysis_label = ttk.Label(window, text="", bootstyle="info", wraplength=700, anchor="w", justify="left")
analysis_label.pack(pady=10)

window.mainloop()
