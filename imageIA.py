# -*- coding: utf-8 -*-
"""
Created on Fri Nov 24 18:18:59 2023

@author: jonat
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import requests
import os
import sys

# Nombre de la búsqueda
if __name__ == "__main__":
    # Obtener la palabra clave de búsqueda desde los argumentos de la línea de comandos
    if len(sys.argv) > 1:
        palabra_clave = sys.argv[1]
    else:
        palabra_clave = input("Ingresa la palabra clave de búsqueda: ")
# Configurar las opciones para ejecutar Chrome en modo sin cabeza
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')  # Necesario si se ejecuta en Windows


try:
    # Inicializar el controlador del navegador
    driver = webdriver.Chrome()
    driver.set_window_size(1366, 768)  # Establecer la resolución a 1366x768

    # Abrir la página de inicio de sesión
    driver.get('https://creator.nightcafe.studio/login?view=password-login')

    # Encontrar el campo de correo electrónico y completarlo
    email_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'email'))
    )
    email_field.send_keys('jonathanmedinah0@gmail.com')
    email_field.send_keys(Keys.RETURN)

    # Encontrar el campo de contraseña y completarlo
    password_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'password'))
    )
    password_field.send_keys('Raspado_1234')
    password_field.send_keys(Keys.RETURN)

    # Hacer clic en el botón de inicio de sesión
    login_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'button[data-testid="SignInSubmitBtn"]'))
    )
    login_button.click()

    # Hacer clic en el botón de creación
    boton_create = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[@class='css-skszrx']//span[@data-testid='CreateBtn']"))
    )
    boton_create.click()

    # Ingresar texto en un campo de texto
    campo_texto = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[@class='css-1fh8jp9']//textarea[@id='promptField']"))
    )
    campo_texto.send_keys("Texto que deseas ingresar")

    # Hacer clic en otro botón de creación
    boton_create = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[@class='css-1taau51']//button[@class='css-1e7lih2']"))
    )
    boton_create.click()

    # Esperar 8 segundos
    time.sleep(8)

    # Encontrar el elemento de la imagen
    image_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "img"))
    )

     # Obtener la URL de la imagen
    image_url = image_element.get_attribute("src")

    # Crear la carpeta "Images_IA" si no existe
    folder_path = os.path.join(os.getcwd(), "Images_IA")
    os.makedirs(folder_path, exist_ok=True)

    # Usar la biblioteca requests para descargar la imagen
    response = requests.get(image_url)
    response.raise_for_status()

    # Guardar la imagen en un archivo con el nombre de la búsqueda
    image_path = os.path.join(folder_path, f"{search_name}_image.jpg")
    with open(image_path, "wb") as file:
        file.write(response.content)

except (TimeoutException, NoSuchElementException) as e:
    print(f"Se produjo una excepción: {e}")

finally:
    # Asegurarse de cerrar el navegador incluso si ocurre una excepción
    if 'driver' in locals():
        driver.quit()