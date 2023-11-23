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

        # Configurar tamaño mínimo para la ventana
        master.minsize(width=650, height=400)

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

        # Canvas para mostrar las imagenes descargadas con la barra de desplazamiento
        self.canvas = tk.Canvas(master)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Configurar la barra de desplazamiento vertical
        self.scrollbar = tk.Scrollbar(master, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Marco para contener las miniaturas de imagenes en el canvas
        self.images_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.images_frame, anchor=tk.NW)

        # Carpeta seleccionada, lista de miniaturas e imagenes seleccionadas
        self.folder_name = ""
        self.images = []
        self.selected_images = []

        # Crear barra lateral para miniaturas y checkboxes
        self.create_sidebar()

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

        # Nueva estructura para organizar las imagenes en filas de tres
        row_num = 0
        col_num = 0
        for i, filename in enumerate(image_files):
            if filename.endswith(".jpg") and i < 20:  # Mostrar solo las primeras 20 imagenes
                img = Image.open(f"{self.folder_name}/{filename}")
                img.thumbnail((200, 200))  # Redimensionar la imagen al tamaño deseado

                # Miniatura de la imagen
                img = ImageTk.PhotoImage(img)
                thumbnail_label = tk.Label(self.images_frame, image=img)
                thumbnail_label.image = img
                thumbnail_label.grid(row=row_num, column=col_num, padx=20, pady=35)

                # Incrementar el número de columna
                col_num += 1

                # Si se alcanza el límite de tres columnas, pasar a la siguiente fila
                if col_num == 3:
                    col_num = 0
                    row_num += 1

                # Agregar miniatura a la lista
                self.images.append((thumbnail_label, img))

        # Actualizar la barra deslizadora después de cargar las imagenes
        self.update_scrollregion()

    def update_scrollregion(self):
        # Método para actualizar la barra deslizadora
        self.canvas.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def create_sidebar(self):
        # Método para crear la barra lateral
        self.sidebar = tk.Frame(self.master, bg='lightgrey', padx=10, pady=10)
        self.sidebar.pack(side=tk.RIGHT, fill=tk.BOTH)

        # Botón para descargar imagenes seleccionadas
        # download_button = tk.Button(self.sidebar, text="Descargar imagenes seleccionadas", command=self.download_selected_images)
        # download_button.grid(row=21, columnspan=2, pady=10)

root = tk.Tk()
app = ImageDownloader(root)
root.mainloop()
