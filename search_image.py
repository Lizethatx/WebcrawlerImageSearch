# -*- coding: utf-8 -*-
import requests
import os
import tkinter as tk
from tkinter import filedialog, messagebox
from bs4 import BeautifulSoup
from PIL import Image, ImageTk
import io

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
        self.button_search = tk.Button(master, text="Buscar imagenes", height=1, width=15, command=self.load_images)
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

        # Carpeta seleccionada y lista de miniaturas
        self.folder_name = ""
        self.images = []

        # Crear barra lateral para miniaturas y checkboxes
        self.create_sidebar()

    def select_folder(self):
        # Método para seleccionar una carpeta
        self.folder_name = filedialog.askdirectory()
        self.label_folder.config(text=f"Carpeta seleccionada: {self.folder_name}")

    def load_images(self):
        # Método para cargar las miniaturas de las imagenes sin descargarlas
        self.clear_images()  # Llamar a clear_images también al inicio de load_images

        # Obtener la palabra clave para la búsqueda
        keywords = self.entry.get()
        url = f"https://www.google.com/search?q={keywords}&source=lnms&tbm=isch"

        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        img_tags = soup.find_all('img')

        # Nueva estructura para organizar las imagenes en filas de tres
        row_num = 0
        col_num = 0
        for i, img in enumerate(img_tags):
            img_url = img['src']
            if img_url.startswith('https') and i < 20:  # Mostrar solo las primeras 20 imagenes
                # Descargar la imagen y convertirla en miniatura
                response = requests.get(img_url)
                img_data = response.content
                img = Image.open(io.BytesIO(img_data))
                img.thumbnail((200, 200))  # Redimensionar la imagen al tamaño deseado

                # Miniatura de la imagen
                img = ImageTk.PhotoImage(img)
                thumbnail_label = tk.Label(self.images_frame, image=img)
                thumbnail_label.image = img
                thumbnail_label.grid(row=row_num, column=col_num, padx=20, pady=15)  # Reducir el espacio vertical

                # Checkbox para cada imagen
                checkbox_var = tk.BooleanVar()
                checkbox = tk.Checkbutton(self.images_frame, variable=checkbox_var)

                # Ajustar el valor de pady para reducir el espacio vertical
                checkbox.grid(row=row_num + 1, column=col_num, pady=(0, 1))

                # Incrementar el número de columna
                col_num += 1

                # Si se alcanza el límite de tres columnas, pasar a la siguiente fila
                if col_num == 3:
                    col_num = 0
                    row_num += 2  # Ajuste para saltar una fila entre las imagenes

                # Agregar miniatura y checkbox a la lista
                self.images.append((thumbnail_label, checkbox, img))

        # Mostrar el botón de descarga después de cargar las imagenes
        download_button = tk.Button(self.master, text="Descargar imagenes seleccionadas", command=self.download_selected_images)
        download_button.pack(pady=(10, 0))

        # Actualizar la barra deslizadora después de cargar las imagenes
        self.update_scrollregion()

    def clear_images(self):
        # Método para destruir los widgets de las imagenes anteriores
        for image, checkbox, _ in self.images:
            image.destroy()
            checkbox.destroy()

    def update_scrollregion(self):
        # Método para actualizar la barra deslizadora
        self.canvas.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def create_sidebar(self):
        # Método para crear la barra lateral
        self.sidebar = tk.Frame(self.master, bg='lightgrey', padx=10, pady=10)
        self.sidebar.pack(side=tk.RIGHT, fill=tk.BOTH)

    def download_selected_images(self):
        # Método para descargar solo las imagenes seleccionadas
        selected_images = [image for image in self.images if image[1].get()]  # Filtrar las imagenes seleccionadas

        if not selected_images:
            messagebox.showinfo("Ninguna imagen seleccionada", "Por favor, seleccione al menos una imagen para descargar.")
            return

        # Crear una carpeta para las imagenes seleccionadas
        selected_folder = os.path.join(self.folder_name, "SelectedImages")
        os.makedirs(selected_folder, exist_ok=True)

        for count, (_, _, img) in enumerate(selected_images):
            # Guardar la imagen seleccionada en la nueva carpeta
            img_path = os.path.join(selected_folder, f"selected_image_{count}.jpg")
            img.save(img_path)

        # Mostrar mensaje de descarga completa
        messagebox.showinfo("Descarga completa", "Las imagenes seleccionadas han sido descargadas en la carpeta SelectedImages.")


root = tk.Tk()
app = ImageDownloader(root)
root.mainloop()
