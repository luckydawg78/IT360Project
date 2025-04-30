import os
import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
from stegano import lsb
from PIL import Image
from PIL.ExifTags import TAGS
import cv2
import numpy as np

def upload_directory():
    directory_path = filedialog.askdirectory()
    if directory_path:
        label.config(text=f"Directory selected: {directory_path}")
        process_directory(directory_path)

def upload_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.png;*.gif")])
    if file_path:
        label.config(text=f"Image selected: {file_path}")
        process_file(file_path)

def process_directory(directory_path):
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.lower().endswith(('.jpg', '.png', '.gif')):
                file_path = os.path.join(root, file)
                process_file(file_path)

def process_file(file_path):
    try:
        # Extract hidden message using LSB steganography
        try:
            hidden_message = lsb.reveal(file_path)
            if hidden_message:
                print(f"Hidden Message in {file_path}:", hidden_message)
                messagebox.showinfo("Hidden Message", f"File: {file_path}\nMessage: {hidden_message}")
            else:
                print(f"No hidden message found in {file_path}.")
        except Exception as e:
            print(f"Error extracting hidden message from {file_path}:", e)

        # Extract EXIF metadata
        try:
            image = Image.open(file_path)
            exif_data = image._getexif()
            if exif_data:
                print(f"\nEXIF Metadata for {file_path}:")
                for tag, value in exif_data.items():
                    tag_name = TAGS.get(tag, tag)
                    print(f"{tag_name:25}: {value}")
        except Exception as e:
            print(f"Error extracting metadata from {file_path}:", e)

        # Read binary data and print last 100 bytes
        try:
            with open(file_path, 'rb') as file:
                data = file.read()
            print(f"\nLast 100 bytes of {file_path}:")
            print(data[-100:])
        except Exception as e:
            print(f"Error reading binary data from {file_path}:", e)

        # Analyze pixel data
        try:
            image = cv2.imread(file_path)
            if image is not None:
                print(f"\nImage Dimensions for {file_path}:", image.shape)
            else:
                print(f"Error: Could not read image {file_path} with OpenCV.")
        except Exception as e:
            print(f"Error analyzing pixel data from {file_path}:", e)
    except Exception as e:
        print(f"Error processing file {file_path}:", e)
        messagebox.showerror("Error", f"Failed to process the file {file_path}.")

# Create GUI
app = tk.Tk()
app.title("Image Analysis Tool")
app.geometry("400x250")

upload_dir_button = tk.Button(app, text="Upload Directory", command=upload_directory)
upload_dir_button.pack(pady=10)

upload_image_button = tk.Button(app, text="Upload Image", command=upload_image)
upload_image_button.pack(pady=10)

label = tk.Label(app, text="No directory or image selected")
label.pack(pady=20)

app.mainloop()


import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageSequence
from stegano import lsb
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

def upload_file():
    global file_path, img_label
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpeg *.jpg *.png")])
    if file_path:
        label.config(text=f"File selected: {file_path}", bootstyle="success")
        img = Image.open(file_path)
        img.thumbnail((400, 400))  # Resize the image to fit within the window
        img = ImageTk.PhotoImage(img)
        img_label.config(image=img)
        img_label.image = img

def embed_message():
    if not file_path:
        analysis_label.config(text="Please upload a file first.", bootstyle="danger")
        return
    message = message_entry.get()
    if not message:
        analysis_label.config(text="Please enter a message to hide.", bootstyle="danger")
        return
    try:
            output_path = file_path.rsplit('.', 1)[0] + "_stego.png"
            lsb.hide(file_path, message).save(output_path)
            analysis_label.config(text=f"Hidden message embedded. Saved to: {output_path}", bootstyle="success")
    except Exception as e:
        analysis_label.config(text=f"Error embedding message: {e}", bootstyle="danger")

window = ttk.Window(themename="superhero")
window.title("Python Steganography")
window.geometry("800x600")

upload_button = ttk.Button(window, text="Upload File", command=upload_file, bootstyle="primary")
upload_button.pack(pady=10)

label = ttk.Label(window, text="No file selected", bootstyle="danger")
label.pack(pady=10)

img_label = ttk.Label(window)
img_label.pack(pady=10)

message_label = ttk.Label(window, text="Enter the message to hide:", bootstyle="info")
message_label.pack(pady=5)

message_entry = ttk.Entry(window, width=35)
message_entry.pack(pady=5)

embed_button = ttk.Button(window, text="Embed Message", command=embed_message, bootstyle="success")
embed_button.pack(pady=10)

analysis_label = ttk.Label(window, text="", bootstyle="info")
analysis_label.pack(pady=10)

window.mainloop()