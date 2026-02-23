import requests
import random
from bs4 import BeautifulSoup


def obtener_producto_aleatorio_total():
    base_url = "https://darpepro.com"

    # =========================
    # MÉTODO 1 → JSON Shopify
    # =========================
    try:
        json_url = f"{base_url}/products.json"
        response = requests.get(json_url, timeout=10)

        if response.status_code == 200:
            data = response.json()
            productos = data.get("products", [])

            if productos:
                producto = random.choice(productos)
                nombre = producto.get("title")
                handle = producto.get("handle")

                url_producto = f"{base_url}/products/{handle}"

                return {
                    "nombre": nombre,
                    "url": url_producto
                }
    except Exception as e:
        print("JSON method failed:", e)

    # =========================
    # MÉTODO 2 → Sitemap XML
    # =========================
    try:
        sitemap_url = f"{base_url}/sitemap_products_1.xml"
        response = requests.get(sitemap_url, timeout=10)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "xml")
            urls = [loc.text for loc in soup.find_all("loc") if "/products/" in loc.text]

            if urls:
                url_producto = random.choice(urls)
                nombre = url_producto.split("/")[-1].replace("-", " ").title()

                return {
                    "nombre": nombre,
                    "url": url_producto
                }
    except Exception as e:
        print("Sitemap method failed:", e)

    # Si ambos fallan
    return None
