import requests
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from time import sleep
import random



options = Options()

#Engañamos al servidor haciendo que selenium parezca humano
options.add_argument("start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")


options.add_argument("--headless")  # No abre ventana
driver = webdriver.Chrome(options=options)


url = "https://www.planetadelibros.com/"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

tema = input("📚 Ingresá una temática (ej: terror, historia, filosofia): ").strip().lower()

# Buscar el enlace correspondiente
links = soup.find_all("a", class_="MenuPrincipalDesktop_nav__linkItem__G87vt")
categoria_url = None

for a in links:
    if tema in a.text.strip().lower():
        categoria_url = a["href"]
        if not categoria_url.startswith("http"):
            categoria_url = "https://www.planetadelibros.com" + categoria_url
        break

if categoria_url:
    print(f"✅ URL encontrada: {categoria_url}")
else:
    print("⚠️ No se encontró esa categoría.")


## ---------------------------------------------

driver.get(categoria_url)
# Esperar hasta que los libros aparezcan (máx. 10 segundos)
try:
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".Libro_libro__YaI5f"))
    )
except:
    print("⚠️ No se cargaron los libros a tiempo.")

books = driver.find_elements(By.CSS_SELECTOR, ".Libro_libro__YaI5f")

if not books:
    print("⚠️ No se encontraron libros en la página.")
else:
    print(f"📚 Se encontraron {len(books)} libros:\n")

    for book in books[:10]:  # limitar a 10
        try:
            title = book.find_element(By.CSS_SELECTOR, "p[class*='Libro_libro__titulo']").text
            author = book.find_element(By.CSS_SELECTOR, "span[class*='LibroAutores_autorNombreTruncado']").text
            link = book.find_element(By.CSS_SELECTOR, "a").get_attribute("href")

            # Entrar a la página del libro
            driver.get(link)
            sleep(random.uniform(1.5, 3.5))  # pausa aleatoria

            try:
                # Buscar el artículo que contiene los párrafos de la sinopsis
                article = driver.find_element(By.CSS_SELECTOR, "div[class*='FichaLibro_sinopsis'] article")

                # Dentro del artículo, tomar el primer <p> que contenga <strong>
                first_p = article.find_element(By.CSS_SELECTOR, "p strong")

                # Obtener el texto del <strong> (sin el resto de los párrafos)
                synopsis = first_p.text.strip()

            except Exception as e:
                synopsis = "Sinopsis no disponible"


            try:
                price = driver.find_element(By.CSS_SELECTOR, "span[class*='PrecioBase_precio']").text
            except:
                price = "Precio no disponible"


            print(f"📘 Título: {title}")
            print(f"👤 Autor: {author}")
            print(f"🔗 Enlace: {link}")
            print("-" * 60)
        except Exception as e:
            print(f"⚠️ Error al procesar libro: {e}")


driver.save_screenshot("debug.png")
print("🖼️ Captura guardada: debug.png")


driver.quit()
