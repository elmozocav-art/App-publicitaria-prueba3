import requests
from bs4 import BeautifulSoup
import random

def obtener_producto_aleatorio_total():
    base_url = "https://darpepro.com"
    # Entramos a la página que lista todos los productos
    collections_url = f"{base_url}/collections/all"
    
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(collections_url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Buscamos todos los contenedores de productos
        # En Shopify suelen ser etiquetas 'a' con una clase específica o dentro de 'product-card'
        productos = soup.find_all('a', href=True)
        
        # Filtramos solo los que son enlaces a productos reales
        enlaces_productos = []
        for p in productos:
            href = p['href']
            # Filtramos para que solo coja enlaces de la carpeta /products/
            if "/products/" in href and href not in enlaces_productos:
                enlaces_productos.append(href)
        
        if not enlaces_productos:
            return {"nombre": "Producto Tecnológico", "url": base_url}

        # Elegimos uno al azar
        link_final = random.choice(enlaces_productos)
        url_completa = base_url + link_final if link_final.startswith('/') else link_final
        
        # Limpiamos el nombre del producto basándonos en el slug de la URL
        nombre_limpio = link_final.split('/')[-1].replace('-', ' ').title()
        
        return {
            "nombre": nombre_limpio,
            "url": url_completa
        }
        
    except Exception as e:
        print(f"Error en scraping: {e}")
        return {"nombre": "Gadget Pro", "url": base_url}
