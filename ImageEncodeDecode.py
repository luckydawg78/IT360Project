import os
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ExifTags
from stegano import lsb
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import cv2
from pprint import pprint

# Initialize global variables
file_path = ""

def get_clean_exif(path):
    """Returns a dict of human-readable EXIF tags (incl. GPS sub-tags)."""
    img = Image.open(path)
    raw_exif = img._getexif() or {}
    clean = {}
    for tag_id, value in raw_exif.items():
        tag = ExifTags.TAGS.get(tag_id, tag_id)
        if tag == "GPSInfo" and isinstance(value, dict):
            gps_data = {}
            for gps_id, gps_val in value.items():
                sub = ExifTags.GPSTAGS.get(gps_id, gps_id)
                gps_data[sub] = gps_val
            clean["GPSInfo"] = gps_data
        else:
            clean[tag] = value
    return clean

def upload_file():
    global file_path
    file_path = filedialog.askopenfilename(
        filetypes=[("Image files", "*.jpeg *.jpg *.png)]
    )
    if not file_path:
        return

    label.config(text=f"File selected: {file_path}", bootstyle="success")

    # Display thumbnail (skip animated GIFs gracefully)
    try:
        img = Image.open(file_path)
        img.thumbnail((400, 400))
        thumb = ImageTk.PhotoImage(img)
        img_label.config(image=thumb)
        img_label.image = thumb
    except Exception:
        img_label.config(image=None)
        img_label.image = None

    process_file(file_path)

def upload_directory():
    directory_path = filedialog.askdirectory()
    if not directory_path:
        return
    label.config(text=f"Directory selected: {directory_path}", bootstyle="success")
    for root, dirs, files in os.walk(directory_path):
        for fn in files:
            if fn.lower().endswith((".jpg", ".jpeg", ".png",)):
                process_file(os.path.join(root, fn))

def embed_message():
    global file_path
    if not file_path:
        analysis_label.config(text="Please upload a file first.", bootstyle="danger")
        return
    msg = message_entry.get().strip()
    if not msg:
        analysis_label.config(text="Please enter a message to hide.", bootstyle="danger")
        return
    if not file_path.lower().endswith((".jpeg", ".jpg", ".png")):
        analysis_label.config(
            text="Unsupported format. Use JPEG or PNG.", bootstyle="danger"
        )
        return
    try:
        out = file_path.rsplit(".", 1)[0] + "_stego.png"
        lsb.hide(file_path, msg).save(out)
        display = out if len(out) <= 50 else out[:50] + "..."
        analysis_label.config(
            text=f"Message embedded → {display}", bootstyle="success"
        )
    except Exception as e:
        analysis_label.config(text=f"Error embedding message: {e}", bootstyle="danger")

def reveal_message():
    global file_path
    if not file_path:
        analysis_label.config(text="Please upload a file first.", bootstyle="danger")
        return
    try:
        hidden = lsb.reveal(file_path)
        if hidden:
            truncated = hidden if len(hidden) <= 50 else hidden[:50] + "..."
            analysis_label.config(text=f"Hidden message: {truncated}", bootstyle="success")
        else:
            analysis_label.config(text="No hidden message found.", bootstyle="warning")
    except ValueError:
        analysis_label.config(text="Invalid image or no hidden message.", bootstyle="danger")
    except Exception as e:
        analysis_label.config(text=f"Error revealing message: {e}", bootstyle="danger")

def process_file(path):
    print(f"\n--- Processing {path} ---")

    # 1) LSB reveal
    try:
        msg = lsb.reveal(path)
        print("LSB →", msg or "(none)")
    except Exception:
        print("LSB → (error or none)")

    # 2) Clean EXIF metadata
    print("\nEXIF metadata:")
    try:
        exif = get_clean_exif(path)
        if exif:
            pprint(exif, width=1)
        else:
            print("  (none)")
    except Exception as e:
        print("Error extracting EXIF:", e)

    # 3) Last 100 bytes of the file
    try:
        with open(path, "rb") as f:
            data = f.read()
        snippet = data[-100:] if len(data) >= 100 else data
        print("\nLast 100 bytes:", snippet)
    except Exception as e:
        print("Error reading binary tail:", e)

    # 4) Image dimensions via OpenCV
    try:
        img_cv = cv2.imread(path)
        if img_cv is None:
            print("OpenCV → could not read image")
        else:
            h, w = img_cv.shape[:2]
            print(f"OpenCV dimensions → {w}x{h}")
    except Exception as e:
        print("OpenCV error:", e)

# GUI Setup
window = ttk.Window(themename="superhero")
window.title("Python Steganography & Analysis Tool")
window.geometry("800x700")

ttk.Button(window, text="Upload Single File", command=upload_file, bootstyle="primary").pack(pady=10)
ttk.Button(window, text="Upload Directory", command=upload_directory, bootstyle="warning").pack(pady=10)

label = ttk.Label(window, text="No file or directory selected", bootstyle="danger")
label.pack(pady=10)

img_label = ttk.Label(window)
img_label.pack(pady=10)

ttk.Label(window, text="Enter message to hide:", bootstyle="info").pack(pady=5)
message_entry = ttk.Entry(window, width=40)
message_entry.pack(pady=5)

ttk.Button(window, text="Embed Message", command=embed_message, bootstyle="success").pack(pady=10)
ttk.Button(window, text="Reveal Message", command=reveal_message, bootstyle="secondary").pack(pady=10)

analysis_label = ttk.Label(window, text="", bootstyle="info", wraplength=700, justify="left")
analysis_label.pack(pady=10)

window.mainloop()
