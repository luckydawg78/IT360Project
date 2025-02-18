import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
from stegano import lsb
from PIL import Image
from PIL.ExifTags import TAGS
import cv2
import numpy as np

def upload_file():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png")])
    if file_path:
        label.config(text=f"File selected: {file_path}")
        process_file(file_path)

def process_file(file_path):
    try:
        # Extract hidden message using LSB steganography
        try:
            hidden_message = lsb.reveal(file_path)
            if hidden_message:
                print("Hidden Message:", hidden_message)
                messagebox.showinfo("Hidden Message", hidden_message)
            else:
                print("No hidden message found.")
        except Exception as e:
            print("Error extracting hidden message:", e)

        # Extract EXIF metadata
        try:
            image = Image.open(file_path)
            exif_data = image._getexif()
            if exif_data:
                print("\nEXIF Metadata:")
                for tag, value in exif_data.items():
                    tag_name = TAGS.get(tag, tag)
                    print(f"{tag_name:25}: {value}")
        except Exception as e:
            print("Error extracting metadata:", e)

        # Read binary data and print last 100 bytes
        try:
            with open(file_path, 'rb') as file:
                data = file.read()
            print("\nLast 100 bytes of file:")
            print(data[-100:])
        except Exception as e:
            print("Error reading binary data:", e)

        # Analyze pixel data
        try:
            image = cv2.imread(file_path)
            if image is not None:
                print("\nImage Dimensions:", image.shape)
            else:
                print("Error: Could not read image with OpenCV.")
        except Exception as e:
            print("Error analyzing pixel data:", e)
    except Exception as e:
        print("Error processing file:", e)
        messagebox.showerror("Error", "Failed to process the selected file.")

# Create GUI
app = tk.Tk()
app.title("Image Analysis Tool")
app.geometry("400x200")

upload_button = tk.Button(app, text="Upload File", command=upload_file)
upload_button.pack(pady=20)

label = tk.Label(app, text="No file selected")
label.pack(pady=20)

app.mainloop()