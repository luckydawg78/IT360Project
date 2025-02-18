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
app.geometry("400x200")

upload_button = tk.Button(app, text="Upload Directory", command=upload_directory)
upload_button.pack(pady=20)

label = tk.Label(app, text="No directory selected")
label.pack(pady=20)

app.mainloop()