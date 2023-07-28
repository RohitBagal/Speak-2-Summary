import tkinter as tk
from PIL import ImageTk, Image
from tkinter import ttk
from urllib.request import urlopen
import requests
import openai
from config import apikey
from io import BytesIO

openai.api_key = apikey


def display_image():
    query = entry.get()
    response = openai.Image.create(
    prompt=query,
    n=1,
    size="1024x1024"
    )
    image_url = response['data'][0]['url']
    print(image_url)
    if image_url:
        try:
            response = requests.get(image_url)
            image_data = response.content
            image = Image.open(BytesIO(image_data))
            image = image.resize((500, 700))  # Resize the image as per your requirement
            photo = ImageTk.PhotoImage(image)
            canvas.create_image(0, 0, anchor=tk.NW, image=photo)
            canvas.image = photo
        except Exception as e:
            # Create the text box to display messages
            text_box = tk.Text(window, height=10, width=50, state='disabled')
            text_box.pack(padx=20, pady=10)
            text_box.configure(state='normal')
            text_box.insert(tk.END, f"Failed to load image: {str(e)}\n")
            text_box.configure(state='disabled')
        entry.delete(0, tk.END)

def reset():
    entry.delete(0, tk.END)
    canvas.delete("all")

# Create the main window
window = tk.Tk()
window.title("Image Viewer")
window.geometry("600x900")  # Set the initial size of the window

# Set background color with an attractive image
bg_image = Image.open("background.jpg")
bg_photo = ImageTk.PhotoImage(bg_image)
bg_label = tk.Label(window, image=bg_photo)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# Add AI Based Image Generator heading
heading_label = tk.Label(window, text="AI Based Image Generator", font=("Arial", 20), fg="white", bg="#4B0082")
heading_label.pack(pady=(20, 10))

# Create the input box
entry = tk.Entry(window, width=50)
entry.pack(padx=20, pady=10)

# Create a frame to hold the buttons
button_frame = tk.Frame(window)
button_frame.pack(pady=(5, 10))

# Add Go icon
go_icon = ImageTk.PhotoImage(Image.open("send.png"))
button_go = tk.Button(button_frame, image=go_icon, command=display_image, bd=0, highlightthickness=0)
button_go.pack(side=tk.LEFT, padx=(20, 5))

# Add Reset icon
reset_icon = ImageTk.PhotoImage(Image.open("reset.png"))
button_reset = tk.Button(button_frame, image=reset_icon, command=reset, bd=0, highlightthickness=0)
button_reset.pack(side=tk.LEFT, padx=(5, 20))

# Create the canvas to display the image
canvas = tk.Canvas(window, width=500, height=700)
canvas.pack(padx=20, pady=10)



# Start the Tkinter event loop
window.mainloop()
