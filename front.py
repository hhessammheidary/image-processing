import tkinter as tk
from tkinter import filedialog
import requests

class ImageUploaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Uploader")

        # Create UI elements
        self.label = tk.Label(root, text="Drag and drop image here:", font=("Helvetica", 12))
        self.label.pack(pady=10)

        self.drop_area = tk.Label(root, text="Drop Area", width=30, height=10, relief="groove", bg="#f0f0f0")
        self.drop_area.pack(pady=5)

        self.upload_button = tk.Button(root, text="Upload", command=self.upload_image, bg="#4caf50", fg="white", font=("Helvetica", 12))
        self.upload_button.pack(pady=5)

        self.response_label = tk.Label(root, text="Response:", font=("Helvetica", 12))
        self.response_label.pack(pady=5)

        self.response_text = tk.Text(root, width=50, height=10, font=("Helvetica", 12))
        self.response_text.pack()

        # Allow dropping files
        self.drop_area.bind("<Button-1>", self.browse_file)
        self.drop_area.bind("<B1-Motion>", self.drag_drop)
        self.drop_area.bind("<ButtonRelease-1>", self.drop)
        
        # Initialize variables
        self.filename = ""

    def browse_file(self, event):
        self.filename = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png *.gif")])

    def drag_drop(self, event):
        self.drop_area.config(text="Drop Here", bg="#c1c1c1")

    def drop(self, event):
        self.drop_area.config(text="Image Dropped", bg="#f0f0f0")

    def upload_image(self):
        if self.filename:
            try:
                files = {'file': open(self.filename, 'rb')}
                response = requests.post("http://127.0.0.1:5000/predict", files=files)
                if response.status_code == 200:
                    self.response_text.delete(1.0, tk.END)
                    self.response_text.insert(tk.END, response.text)
                else:
                    self.response_text.delete(1.0, tk.END)
                    self.response_text.insert(tk.END, f"Error: {response.status_code}")
            except Exception as e:
                self.response_text.delete(1.0, tk.END)
                self.response_text.insert(tk.END, f"Error: {e}")
        else:
            self.response_text.delete(1.0, tk.END)
            self.response_text.insert(tk.END, "Please select an image file.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageUploaderApp(root)
    root.mainloop()
