
import tkinter as tk
from tkinter import filedialog
from stegano import lsb

def upload_file():
    global file_path
    file_path = filedialog.askopenfilename(filetypes=[("Images", "*.jpeg *.jpg *.png *.gif")])
    if file_path:
        label.config(text=f"File selected: {file_path}", fg="black", bg="green")

def embed_message():
    if not file_path:
        analysis_label.config(text="Please enter text to hide.", fg="black", bg="red")
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


window = tk.Tk()
window.title("Python Steganography")
window.configure(bg='#525252')

upload_button = tk.Button(window, text="Upload File", command=upload_file)
upload_button.pack(pady=10)

label = tk.Label(window, text="No file selected", fg="black", bg="red")
label.pack(pady=10)

message_label = tk.Label(window, text="Enter the message to hide:", fg="white", bg="#525252")
message_label.pack(pady=5)

message_entry = tk.Entry(window, width=35)
message_entry.pack(pady=5)

embed_button = tk.Button(window, text="Embed Message", command=embed_message)
embed_button.pack(pady=10)

analysis_label = tk.Label(window, text="", bg='#525252', fg="red")
analysis_label.pack(pady=10)

window.mainloop()

