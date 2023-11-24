# -*- coding: utf-8 -*-
import requests
import os
import tkinter as tk
from tkinter import filedialog, messagebox
from bs4 import BeautifulSoup
from PIL import Image, ImageTk, UnidentifiedImageError
import io

class ImageDownloader:
    def __init__(self, master):
        self.master = master
        master.title("Buscador de Imagenes")

        # Configurar tamaño mínimo para la ventana
        master.minsize(width=850, height=500)

        # Etiqueta y entrada para la palabra de búsqueda
        self.label = tk.Label(master, text="Ingresa la imagen a buscar:")
        self.label.pack(padx=10, pady=10)
        self.entry = tk.Entry(master)
        self.entry.pack(padx=10, pady=10)

        # Botón para buscar imagenes
        self.button_search = tk.Button(master, text="Buscar imagenes", height=1, width=15, command=self.load_images)
        self.button_search.pack(side=tk.TOP, pady=(10, 0))

        # Marco para contener las miniaturas de imágenes y la barra de desplazamiento en el lienzo
        self.images_frame = tk.Frame(master)
        self.images_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Lienzo para mostrar las imágenes descargadas con la barra de desplazamiento
        self.canvas = tk.Canvas(self.images_frame)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Configurar la barra de desplazamiento vertical
        self.scrollbar = tk.Scrollbar(self.images_frame, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Lista para almacenar imagenes y sus datos
        self.images = []
        self.image_data_list = []

        # Carpeta seleccionada
        self.folder_name = ""

        # Crear el control deslizante y su etiqueta
        self.image_count_label = tk.Label(master, text="Numero de imagenes:")
        self.image_count_label.pack(pady=(100, 5))

        self.image_count_var = tk.IntVar(value=20)  # Valor predeterminado
        self.image_count_slider = tk.Scale(master, from_=1, to=50, orient=tk.HORIZONTAL, variable=self.image_count_var, length=150)
        self.image_count_slider.pack(pady=(0, 10))

        # Botón para descargar imagenes seleccionadas
        self.download_button = tk.Button(master, text="Descargar imagenes seleccionadas", command=self.download_selected_images)
        self.download_button.pack(padx=10, pady=25)
        self.download_button.config(state=tk.DISABLED)  # Deshabilitar el botón al inicio

    def load_images(self):
        # Método para cargar las miniaturas de las imagenes sin descargarlas
        self.download_button.config(state=tk.DISABLED)  # Deshabilitar el botón al inicio
        self.clear_images()  # Llamar a clear_images también al inicio de load_images
        self.image_data_list = []

        # Obtener el número de imagenes deseadas del slider
        num_images = self.image_count_var.get()

        # Obtener la palabra clave para la búsqueda
        self.keywords = self.entry.get()
        url = f"https://www.google.com/search?q={self.keywords}&source=lnms&tbm=isch"

        try:
            response = requests.get(url)
            response.raise_for_status()  # Verificar si la solicitud fue exitosa
            soup = BeautifulSoup(response.text, 'html.parser')
            img_tags = soup.find_all('img')

            # Nueva estructura para organizar las imagenes en filas de tres
            row_num = 0
            col_num = 0
            self.images = [] 
            for i, img in enumerate(img_tags):
                img_url = img['src']
                if img_url.startswith('https') and i < num_images+1:
                    try:
                        # Descargar la imagen y almacenar sus datos
                        response = requests.get(img_url)
                        response.raise_for_status()  # Verificar si la solicitud fue exitosa
                        img_data = response.content
                        img_original = Image.open(io.BytesIO(img_data))

                        # Almacenar la imagen y sus datos en la lista
                        self.image_data_list.append((img_original, img_data))

                        # Miniatura de la imagen
                        img_tk = ImageTk.PhotoImage(img_original)
                        thumbnail_label = tk.Label(self.canvas, image=img_tk)
                        thumbnail_label.image = img_tk
                        thumbnail_label.grid(row=row_num, column=col_num, padx=20, pady=15)  # Reducir el espacio vertical

                        # Checkbox para cada imagen
                        checkbox_var = tk.BooleanVar()
                        checkbox = tk.Checkbutton(self.canvas, variable=checkbox_var)

                        # Asegúrate de almacenar la variable en la tupla de imagenes
                        self.images.append((thumbnail_label, checkbox_var, img_original, img_tk))  # Almacenar la imagen original y PhotoImage

                        # Ajustar el valor de pady para reducir el espacio vertical
                        checkbox.grid(row=row_num + 1, column=col_num, pady=(0, 1))

                        # Incrementar el número de columna
                        col_num += 1

                        # Si se alcanza el límite de tres columnas, pasar a la siguiente fila
                        if col_num == 3:
                            col_num = 0
                            row_num += 2  # Ajuste para saltar una fila entre las imagenes

                    except (UnidentifiedImageError, requests.RequestException) as e:
                        # Capturar y manejar errores de imagenes no identificadas o problemas de solicitud
                        print(f"Error al procesar la imagen {img_url}: {e}")

        except requests.RequestException as e:
            # Capturar y manejar problemas de solicitud al obtener la página web
            print(f"Error en la solicitud HTTP: {e}")


        # Habilitar el botón de descarga después de cargar las imagenes
        self.download_button.config(state=tk.NORMAL)

        # Mostrar el botón de descarga después de cargar las imagenes
        self.update_scrollregion()

    def clear_images(self):
        # Método para destruir los widgets de las imágenes anteriores
        for thumbnail_label, checkbox_var, _, _ in self.images:
            thumbnail_label.destroy()
            checkbox_var.set(False)  # Deseleccionar la casilla de verificación

        # Limpiar la lista de imagenes
        self.images = []

    def update_scrollregion(self):
        # Método para actualizar la barra deslizadora
        self.canvas.update_idletasks()

        # Obtener el ancho y la altura total del contenido en el lienzo
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        bbox = self.canvas.bbox(tk.ALL)

        # Ajustar el área de desplazamiento solo si hay contenido en el lienzo
        if bbox:
            self.canvas.config(scrollregion=(0, 0, max(canvas_width, bbox[2]), max(canvas_height, bbox[3])))


    def download_selected_images(self):
        selected_images = [image for image in self.images if image[1].get()]

        if not selected_images:
            messagebox.showinfo("Ninguna imagen seleccionada", "Por favor, seleccione al menos una imagen para descargar.")
            return

        # Crear una carpeta para las imagenes seleccionadas
        self.folder_name = filedialog.askdirectory()
        selected_folder = os.path.join(self.folder_name, f"{self.keywords}_Images")
        os.makedirs(selected_folder, exist_ok=True)

        for count, selected_image in enumerate(selected_images):
            (_, _, img_original, _) = selected_image
            # Obtener el dato de la imagen original desde la lista
            img_data = self.image_data_list[count][1]

            # Obtener el formato de la imagen original
            img_format = img_original.format.lower() if img_original.format else 'png'

            # Guardar la imagen seleccionada en la nueva carpeta con el formato correcto
            img_path = os.path.join(selected_folder, f"image_{count+1}.{img_format}")
            with open(img_path, 'wb') as img_file:
                img_file.write(img_data)

        # Mostrar mensaje de descarga completa
        messagebox.showinfo("Descarga completa", f"Las imagenes seleccionadas han sido descargadas en la carpeta {self.keywords}_Images.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageDownloader(root)
    root.mainloop()
