import tkinter as tk
from tkinter import filedialog
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

app = tk.Tk()
app.title("File Upload GUI")

upload_button = tk.Button(app, text="Upload File", command=upload_file)
upload_button.pack(pady=20)

label = tk.Label(app, text="No file selected")
label.pack(pady=20)

app.mainloop()



hidden_message = lsb.reveal('file_path')
print (hidden_message)

image = image.open('file_path')
exif_data = image._getexif()

if exif_data:
    for tag, value in exif_data.items():
        tag_name = TAGS.get(tag, tag)
        print(f"{tag_name:25}: {value}")    

with open('file_path', 'wb') as file:
    data = file.read()
print(data[-100:])  # Print last 100 bytes



image = cv2.imread("image.png")
print(image.shape)  # Analyze pixel values for anomalies