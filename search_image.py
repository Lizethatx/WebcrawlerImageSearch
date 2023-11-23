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

        # Etiqueta y entrada para la palabra de búsqueda
        self.label = tk.Label(master, text="Ingresa la imagen a buscar:")
        self.label.pack(padx=10, pady=10)
        self.entry = tk.Entry(master)
        self.entry.pack(padx=10, pady=10)

        # Botón para buscar imagenes
        self.button_search = tk.Button(master, text="Buscar imagenes", height=1, width=15, command=self.load_images)
        self.button_search.pack(side=tk.TOP, pady=(10, 0))

        # Canvas para mostrar las imagenes descargadas con la barra de desplazamiento
        self.canvas = tk.Canvas(master)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Crear botón para descargar imagenes seleccionadas
        self.download_button = tk.Button(self.master, text="Descargar imagenes seleccionadas", command=self.download_selected_images)
        self.download_button.pack(side=tk.LEFT, padx=10, pady=10)
        self.download_button.config(state=tk.DISABLED)  # Deshabilitar el botón al inicio

        # Configurar la barra de desplazamiento vertical
        self.scrollbar = tk.Scrollbar(master, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Marco para contener las miniaturas de imagenes en el canvas
        self.images_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 5), window=self.images_frame, anchor=tk.NW)

        # Lista para almacenar imagenes y sus datos
        self.images = []
        self.image_data_list = []

        # Crear barra lateral para miniaturas y checkboxes
        self.create_sidebar()

        # Carpeta seleccionada
        self.folder_name = ""

    def load_images(self):
        # Método para cargar las miniaturas de las imagenes sin descargarlas
        self.download_button.config(state=tk.DISABLED)  # Deshabilitar el botón al inicio
        self.clear_images()  # Llamar a clear_images también al inicio de load_images
        self.image_data_list = []
        

        # Obtener la palabra clave para la búsqueda
        self.keywords = self.entry.get()
        url = f"https://www.google.com/search?q={self.keywords}&source=lnms&tbm=isch"

        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        img_tags = soup.find_all('img')

        # Nueva estructura para organizar las imagenes en filas de tres
        row_num = 0
        col_num = 0
        for i, img in enumerate(img_tags):
            img_url = img['src']
            if img_url.startswith('https') and i < 20:
                # Descargar la imagen y almacenar sus datos
                response = requests.get(img_url)
                img_data = response.content
                img_original = Image.open(io.BytesIO(img_data))

                # Almacenar la imagen y sus datos en la lista
                self.image_data_list.append((img_original, img_data))
                img_original.thumbnail((200, 200))  # Redimensionar la imagen al tamaño deseado

                # Miniatura de la imagen
                img = ImageTk.PhotoImage(img_original)
                thumbnail_label = tk.Label(self.images_frame, image=img)
                thumbnail_label.image = img
                thumbnail_label.grid(row=row_num, column=col_num, padx=20, pady=15)  # Reducir el espacio vertical

                # Checkbox para cada imagen
                checkbox_var = tk.BooleanVar()
                checkbox = tk.Checkbutton(self.images_frame, variable=checkbox_var)

                # Asegúrate de almacenar la variable en la tupla de imagenes
                self.images.append((thumbnail_label, checkbox_var, img))

                # Ajustar el valor de pady para reducir el espacio vertical
                checkbox.grid(row=row_num + 1, column=col_num, pady=(0, 1))

                # Incrementar el número de columna
                col_num += 1

                # Si se alcanza el límite de tres columnas, pasar a la siguiente fila
                if col_num == 3:
                    col_num = 0
                    row_num += 2  # Ajuste para saltar una fila entre las imagenes

        # Habilitar el botón de descarga después de cargar las imagenes
        self.download_button.config(state=tk.NORMAL)

        # Mostrar el botón de descarga después de cargar las imagenes
        self.update_scrollregion()

        # Mostrar el botón de descarga después de cargar las imagenes
        self.update_scrollregion()

    def clear_images(self):
        # Método para destruir los widgets de las imágenes anteriores
        for thumbnail_label, checkbox_var, img_widget in self.images:
            thumbnail_label.destroy()
            checkbox_var.set(False)  # Deseleccionar la casilla de verificación

        # Limpiar la lista de imágenes
        self.images = []

    def update_scrollregion(self):
        # Método para actualizar la barra deslizadora
        self.canvas.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def create_sidebar(self):
        # Método para crear la barra lateral
        self.sidebar = tk.Frame(self.images_frame, bg='lightgrey', padx=10, pady=10)
        self.sidebar.grid(row=0, column=3, rowspan=100, sticky="n")

    def download_selected_images(self):
        # Método para descargar solo las imagenes seleccionadas
        selected_images = [image for image in self.images if image[1].get()]  # Filtrar las imagenes seleccionadas

        if not selected_images:
            messagebox.showinfo("Ninguna imagen seleccionada", "Por favor, seleccione al menos una imagen para descargar.")
            return

        # Crear una carpeta para las imagenes seleccionadas
        self.folder_name = filedialog.askdirectory()
        selected_folder = os.path.join(self.folder_name, f"{self.keywords}_Images")
        os.makedirs(selected_folder, exist_ok=True)

        for count, (_, checkbox_var, img) in enumerate(selected_images):
            # Obtener el dato de la imagen original desde la lista
            img_original, img_data = self.image_data_list[count]

            # Guardar la imagen seleccionada en la nueva carpeta
            img_path = os.path.join(selected_folder, f"image_{count+1}.jpg")
            img_original.save(img_path)

        # Mostrar mensaje de descarga completa
        messagebox.showinfo("Descarga completa", f"Las imagenes seleccionadas han sido descargadas en la carpeta {self.keywords}_Images.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageDownloader(root)
    root.mainloop()
