import requests
import random


def obtener_producto_aleatorio_total():
    base_url = "https://darpepro.com"
    productos_totales = []

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        page = 1

        # Intentamos traer hasta 5 páginas (ajustable)
        while page <= 5:
            url = f"{base_url}/products.json?limit=250&page={page}"
            response = requests.get(url, headers=headers, timeout=10)

            if response.status_code != 200:
                break

            data = response.json()
            productos = data.get("products", [])

            if not productos:
                break

            productos_totales.extend(productos)
            page += 1

        if not productos_totales:
            print("No se encontraron productos en JSON.")
            return None

        producto = random.choice(productos_totales)

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

