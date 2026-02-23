import requests
from bs4 import BeautifulSoup
import random


def obtener_producto_aleatorio_total():
    base_url = "https://darpepro.com"
    collections_url = f"{base_url}/collections/all"

    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = requests.get(collections_url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # Buscar tarjetas reales de productos
        productos = soup.select("a[href*='/products/']")

        enlaces_validos = []
        for a in productos:
            href = a.get("href")
            if href and "/products/" in href:
                enlaces_validos.append(href)

        enlaces_validos = list(set(enlaces_validos))

        if not enlaces_validos:
            return None  # Si falla, no devolvemos la home

        link_final = random.choice(enlaces_validos)
        url_producto = base_url + link_final if link_final.startswith("/") else link_final

        # 🔎 Ahora entramos en la página del producto para sacar el nombre real
        response_producto = requests.get(url_producto, headers=headers)
        soup_producto = BeautifulSoup(response_producto.text, "html.parser")

        titulo = soup_producto.find("h1")
        nombre_real = titulo.get_text(strip=True) if titulo else "Producto DarpePro"

        return {
            "nombre": nombre_real,
            "url": url_producto
        }

    except Exception as e:
        print("Error scraper:", e)
        return None

