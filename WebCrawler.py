import requests
import os
import tkinter as tk
from tkinter import filedialog
from bs4 import BeautifulSoup
from PIL import Image, ImageTk

class ImageDownloader:
    def __init__(self, master):
        self.master = master
        master.title("Web Crawler-JAF")

        self.button_folder = tk.Button(master, text="Seleccionar carpeta", command=self.select_folder)
        self.button_folder.pack(padx=10, pady=10)

        self.label_folder = tk.Label(master, text="Selecciona una carpeta de destino para las imágenes descargadas:")
        self.label_folder.pack(padx=10, pady=10)
        
        self.label = tk.Label(master, text="Ingresa la palabra para la búsqueda:")
        self.label.pack(padx=10, pady=10)
               
        self.entry = tk.Entry(master)
        self.entry.pack(padx=1, pady=1)
        
        self.button_search = tk.Button(master, text="Buscar imágenes", height = 1, width = 15, command=self.search_images)
        self.button_search.pack(padx=10, pady=10)
        
        self.images_frame = tk.Frame(master)
        self.images_frame.pack(padx=10, pady=10)

        self.images = []

    def search_images(self):

        keywords = self.entry.get()

        url = f"https://www.google.com/search?q={keywords}&source=lnms&tbm=isch"

        response = requests.get(url)

        soup = BeautifulSoup(response.text, 'html.parser')

        img_tags = soup.find_all('img')

        count = 0
        for img in img_tags:
            img_url = img['src']
            if img_url.startswith('https'):
                response = requests.get(img_url)
                with open(f"{self.folder_name}/image_{count}.jpg", "wb") as f:
                    f.write(response.content)
                count += 1

        self.load_images()

    def select_folder(self):
        self.folder_name = filedialog.askdirectory()
        self.label_folder.config(text=f"Carpeta seleccionada: {self.folder_name}")

    def load_images(self):
        for image in self.images:
            image.destroy()
        image_files = os.listdir(self.folder_name)

        for filename in image_files:
            if filename.endswith(".jpg"):
                img = Image.open(f"{self.folder_name}/{filename}")
                img = img.resize((150, 150))
                img = ImageTk.PhotoImage(img)
                label = tk.Label(self.images_frame, image=img)
                label.image = img
                label.pack()
                self.images.append(label)

root = tk.Tk()
app = ImageDownloader(root)
root.mainloop()
