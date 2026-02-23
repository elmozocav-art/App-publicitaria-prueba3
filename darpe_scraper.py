import requests
import random
from bs4 import BeautifulSoup


def obtener_producto_aleatorio_total():
    base_url = "https://darpepro.com"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "es-ES,es;q=0.9,en;q=0.8",
        "Connection": "keep-alive"
    }

    try:
        # Entramos a la colección general
        url = f"{base_url}/collections/all"
        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code != 200:
            print("Status code:", response.status_code)
            return None

        soup = BeautifulSoup(response.text, "html.parser")

        enlaces = []

        for a in soup.find_all("a", href=True):
            href = a["href"]
            if "/products/" in href:
                if href.startswith("/"):
                    enlaces.append(base_url + href)
                else:
                    enlaces.append(href)

        enlaces = list(set(enlaces))

        if not enlaces:
            print("No se encontraron enlaces de productos.")
            return None

        url_producto = random.choice(enlaces)

        # Entramos en la página del producto elegido
        response_producto = requests.get(url_producto, headers=headers, timeout=10)
        soup_producto = BeautifulSoup(response_producto.text, "html.parser")

        titulo = soup_producto.find("h1")
        nombre = titulo.get_text(strip=True) if titulo else "Producto DarpePro"

        return {
            "nombre": nombre,
            "url": url_producto
        }

    except Exception as e:
        print("Error scraper:", e)
        return None


