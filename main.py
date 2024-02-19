import tkinter as tk
from tkinter import ttk, messagebox
import requests
from PIL import Image, ImageTk
from io import BytesIO
from datetime import date

today = date.today()

class NASA_App:
    def __init__(self, root):
        self.root = root
        self.root.title("NASA astronomy picture of the day")
        self.root.geometry("900x700")
        self.create_widgets()

    def create_widgets(self):
        self.frame = ttk.Frame(self.root)
        self.frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.label_title = ttk.Label(self.frame, text="Nasa astronomy picture of the day", font=("Arial",20))
        self.label_title.pack(pady=10)

        self.button_load = ttk.Button(self.frame, text="Load Picture", command=self.load_apod)
        self.button_load.pack(pady=10)

        self.image_label_frame = ttk.Frame(self.frame)
        self.image_label_frame.pack(fill=tk.BOTH, expand=True)
        self.image_label = ttk.Label(self.image_label_frame)
        self.image_label.pack(pady=10)

        self.scrollbar = ttk.Scrollbar(self.frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.description_text = tk.Text(self.frame, height=10, wrap="word", yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.description_text.yview)
        self.description_text.pack(pady=10, fill=tk.BOTH, expand=True)

        root.config(bg="gray")

    def load_apod(self):
        api_key = "DEMO_KEY"
        url = f"https://api.nasa.gov/planetary/apod?date={today}&api_key={api_key}"

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            image_url = data["url"]
            image_response = requests.get(image_url)
            image = Image.open(BytesIO(image_response.content))
            max_size = (500, 400)
            image.thumbnail(max_size, Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(image)

            self.image_label.configure(image=photo)
            self.image_label.image = photo
            
            self.description_text.delete(1.0, tk.END)
            self.description_text.insert(tk.END, f"{data["title"]}\n\n{data["explanation"]}")
    
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load data: {e}")
        
        else: 
            messagebox.showinfo("Success!", "APOD data loaded sucsessfully")
    

if __name__ == "__main__":
    root = tk.Tk()
    app = NASA_App(root)
    root.mainloop()