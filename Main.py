import tkinter as tk
from tkinter import filedialog
from stegano import lsb

def upload_file():
    global file_path
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpeg *.jpg *.png")])
    if file_path:
        label.config(text=f"File selected: {file_path}")

def embed_message():
    if not file_path:
        analysis_label.config(text="Please upload a file first.")
        return
    message = message_entry.get()
    if not message:
        analysis_label.config(text="Please enter a message to hide.")
        return
    try:
        output_path = file_path.rsplit('.', 1)[0] + "_stego.png"
        lsb.hide(file_path, message).save(output_path)
        analysis_label.config(text=f"Hidden message embedded. Saved to: {output_path}")
    except Exception as e:
        analysis_label.config(text=f"Error embedding message: {e}")

app = tk.Tk()
app.title("File Upload and Steganography Embed GUI")

upload_button = tk.Button(app, text="Upload File", command=upload_file)
upload_button.pack(pady=20)

label = tk.Label(app, text="No file selected")
label.pack(pady=20)

message_label = tk.Label(app, text="Enter the message to hide:")
message_label.pack(pady=10)

message_entry = tk.Entry(app, width=50)
message_entry.pack(pady=10)

embed_button = tk.Button(app, text="Embed Message", command=embed_message)
embed_button.pack(pady=10)

analysis_label = tk.Label(app, text="")
analysis_label.pack(pady=20)

app.mainloop()