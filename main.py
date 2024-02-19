import tkinter as tk
from tkinter import ttk, messagebox
import requests
from PIL import Image, ImageTk
from io import BytesIO
from datetime import date

# Get today's date
today = date.today()

class NASA_App:
    def __init__(self, root):
        # Initialize the application window
        self.root = root
        self.root.title("NASA astronomy picture of the day")  # Set window title
        self.root.geometry("900x700")  # Set window size
        self.create_widgets()  # Create GUI widgets

    def create_widgets(self):
        # Create main frame
        self.frame = ttk.Frame(self.root)
        self.frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Title label
        self.label_title = ttk.Label(self.frame, text="Nasa astronomy picture of the day", font=("Arial", 20))
        self.label_title.pack(pady=10)

        # Button to load picture
        self.button_load = ttk.Button(self.frame, text="Load Picture", command=self.load_apod)
        self.button_load.pack(pady=10)

        # Frame to display image
        self.image_label_frame = ttk.Frame(self.frame)
        self.image_label_frame.pack(fill=tk.BOTH, expand=True)
        self.image_label = ttk.Label(self.image_label_frame)
        self.image_label.pack(pady=10)

        # Scrollbar for description text
        self.scrollbar = ttk.Scrollbar(self.frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Description text area
        self.description_text = tk.Text(self.frame, height=10, wrap="word", yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.description_text.yview)
        self.description_text.pack(pady=10, fill=tk.BOTH, expand=True)

        # Set background color
        root.config(bg="gray")

    def load_apod(self):
        # API key for NASA API
        api_key = "DEMO_KEY"
        
        # The API link
        url = f"https://api.nasa.gov/planetary/apod?date={today}&api_key={api_key}"

        try:
            # Send request to NASA API
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            # Get image URL and download the image
            image_url = data["url"]
            image_response = requests.get(image_url)
            image = Image.open(BytesIO(image_response.content))

            # Resize image
            max_size = (500, 400)
            image.thumbnail(max_size, Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(image)

            # Display image in GUI
            self.image_label.configure(image=photo)
            self.image_label.image = photo
            
            # Display title and explanation in the description text area
            self.description_text.delete(1.0, tk.END)
            self.description_text.insert(tk.END, f"{data['title']}\n\n{data['explanation']}")

        except Exception as e:

            messagebox.showerror("Error", f"Failed to load data: {e}")
        
        else: 

            messagebox.showinfo("Success!", "APOD data loaded successfully")

# Main function to run the application
if __name__ == "__main__":
    root = tk.Tk()  
    app = NASA_App(root)  
    root.mainloop()
