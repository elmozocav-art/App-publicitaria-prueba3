import requests
import random


def obtener_producto_aleatorio_total():
    base_url = "https://darpepro.com"
    json_url = f"{base_url}/collections/all/products.json"

    try:
        response = requests.get(json_url)
        response.raise_for_status()
        data = response.json()

        productos = data.get("products", [])

        if not productos:
            return None

        producto = random.choice(productos)

        nombre = producto.get("title")
        handle = producto.get("handle")

        url_producto = f"{base_url}/products/{handle}"

        return {
            "nombre": nombre,
            "url": url_producto
        }

    except Exception as e:
        print("Error scraper:", e)
        return None
