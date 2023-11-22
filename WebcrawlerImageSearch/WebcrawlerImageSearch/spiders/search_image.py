# -*- coding: utf-8 -*-
import requests
import os
import tkinter as tk
from tkinter import filedialog, messagebox
from bs4 import BeautifulSoup
from PIL import Image, ImageTk

class ImageDownloader:
    def __init__(self, master):
        self.master = master
        master.title("Web Crawler-JAF")

        # Botón para seleccionar carpeta
        self.button_folder = tk.Button(master, text="Seleccionar carpeta", command=self.select_folder)
        self.button_folder.pack(padx=10, pady=10)

        # Etiqueta que muestra la carpeta seleccionada
        self.label_folder = tk.Label(master, text="Selecciona una carpeta de destino para las imagenes descargadas:")
        self.label_folder.pack(padx=10, pady=10)

        # Etiqueta y entrada para la palabra de búsqueda
        self.label = tk.Label(master, text="Ingresa la palabra para la busqueda:")
        self.label.pack(padx=10, pady=10)
        self.entry = tk.Entry(master)
        self.entry.pack(padx=1, pady=1)

        # Botón para buscar imagenes
        self.button_search = tk.Button(master, text="Buscar imagenes", height=1, width=15, command=self.search_images)
        self.button_search.pack(padx=10, pady=10)

        # Marco para mostrar las imagenes descargadas
        self.images_frame = tk.Frame(master)
        self.images_frame.pack(padx=10, pady=10)

        # Carpeta seleccionada, lista de miniaturas e imagenes seleccionadas
        self.folder_name = ""
        self.images = []
        self.selected_images = []

        # Crear barra lateral para miniaturas y checkboxes
        self.create_sidebar()

        # Configurar evento de cambio de tamaño de ventana
        master.bind('<Configure>', self.resize_images)

    def search_images(self):
        # Método para buscar e descargar imagenes
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
        # Método para seleccionar una carpeta
        self.folder_name = filedialog.askdirectory()
        self.label_folder.config(text=f"Carpeta seleccionada: {self.folder_name}")

    def load_images(self):
        # Método para cargar las miniaturas de las imagenes descargadas
        for image in self.images:
            image[0].destroy()
            image[1].destroy()
        self.images = []  # Limpiar lista de miniaturas
        image_files = os.listdir(self.folder_name)

        for i, filename in enumerate(image_files):
            if filename.endswith(".jpg") and i < 20:  # Mostrar solo las primeras 20 imagenes
                img = Image.open(f"{self.folder_name}/{filename}")
                img.thumbnail((150, 150))  # Redimensionar la imagen al tamaño deseado

                # Checkbox para cada imagen
                checkbox_var = tk.BooleanVar()
                checkbox = tk.Checkbutton(self.sidebar, variable=checkbox_var)
                checkbox.checkbox_var = checkbox_var
                checkbox.grid(row=i, column=0, pady=5)

                # Miniatura de la imagen
                img = ImageTk.PhotoImage(img)
                thumbnail_label = tk.Label(self.sidebar, image=img)
                thumbnail_label.image = img
                thumbnail_label.grid(row=i, column=1, pady=5)

                # Agregar checkbox y miniatura a la lista
                self.images.append((checkbox, thumbnail_label, img))

    def create_sidebar(self):
        # Método para crear la barra lateral
        self.sidebar = tk.Frame(self.master, bg='lightgrey', padx=10, pady=10)
        self.sidebar.pack(side=tk.RIGHT, fill=tk.BOTH)

        # Botón para descargar imagenes seleccionadas
        download_button = tk.Button(self.sidebar, text="Descargar imagenes seleccionadas", command=self.download_selected_images)
        download_button.grid(row=21, columnspan=2, pady=10)

    def download_selected_images(self):
        # Método para descargar solo las imagenes seleccionadas
        self.selected_images = [image for image in self.images if image[0].checkbox_var.get()]

        for count, (_, _, img) in enumerate(self.selected_images):
            response = requests.get(img)
            with open(f"{self.folder_name}/selected_image_{count}.jpg", "wb") as f:
                f.write(response.content)

        # Mostrar mensaje de descarga completa
        messagebox.showinfo("Descarga completa", "Las imagenes seleccionadas han sido descargadas.")

    def resize_images(self, event):
        # Método para redimensionar las imagenes de acuerdo al tamaño de la ventana
        new_width = event.width // 4  # Dividir el ancho de la ventana en 4
        new_height = event.height // 20  # Dividir el alto de la ventana en 20

        for _, thumbnail_label, img in self.images:
            resized_img = img.subsample(new_width, new_height)
            thumbnail_label.configure(image=resized_img)
            thumbnail_label.image = resized_img

root = tk.Tk()
app = ImageDownloader(root)
root.mainloop()

