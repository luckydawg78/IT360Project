import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
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
window.geometry("800x700")

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

