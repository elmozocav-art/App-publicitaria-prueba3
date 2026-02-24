import requests
import random


def obtener_producto_aleatorio_total():
    base_url = "https://darpepro.com"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        url = f"{base_url}/products.json?limit=250"
        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code == 200:
            data = response.json()
            productos = data.get("products", [])

            if productos:
                producto = random.choice(productos)

                nombre = producto.get("title", "Producto DarpePro")
                handle = producto.get("handle")

                if handle:
                    url_producto = f"{base_url}/products/{handle}"
                else:
                    url_producto = base_url

                return {
                    "nombre": nombre,
                    "url": url_producto
                }

        print("No se pudieron obtener productos reales.")

    except Exception as e:
        print("Error scraper:", e)

    # 🔥 FALLBACK SEGURO (Nunca devuelve None)
    return {
        "nombre": "Producto Destacado DarpePro",
        "url": base_url
    }
