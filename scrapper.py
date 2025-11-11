import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

options = Options()
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)

tema = "terror"
driver.get(f"https://www.planetadelibros.com/libros/{tema}/00012")

time.sleep(5)  # Esperar 5 segundos a que cargue todo
print(driver.current_url)  # Mostrar URL final
print(driver.page_source[:1000])  # Mostrar parte del HTML


# Espera que aparezcan los libros
WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a[href*='/libro/']"))
)

html = driver.page_source
soup = BeautifulSoup(html, "html.parser")

for link in soup.select("a[href*='/libro/']")[:10]:
    titulo = link.get("title") or link.text.strip()
    print("📘", titulo)

driver.quit()
