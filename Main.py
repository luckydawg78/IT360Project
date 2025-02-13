import tkinter as tk
from tkinter import filedialog

def upload_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        label.config(text=f"File selected: {file_path}")

app = tk.Tk()
app.title("File Upload GUI")

upload_button = tk.Button(app, text="Upload File", command=upload_file)
upload_button.pack(pady=20)

label = tk.Label(app, text="No file selected")
label.pack(pady=20)

app.mainloop()