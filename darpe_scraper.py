import requests
from bs4 import BeautifulSoup
import random

def obtener_producto_aleatorio_total():
    base_url = "https://darpepro.com"
    collections_url = f"{base_url}/collections/all"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        response = requests.get(collections_url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 1. Buscamos todos los enlaces de productos específicos
        # En DarpePro (Shopify), los productos suelen estar en etiquetas <a> que contienen '/products/'
        enlaces = soup.find_all('a', href=True)
        links_validos = []
        
        for a in enlaces:
            href = a['href']
            # Filtramos para que sea un producto y no una colección o búsqueda
            if "/products/" in href and "collections" not in href and "/products/apple-pay" not in href:
                full_url = href if href.startswith('http') else base_url + href
                links_validos.append(full_url)
        
        # Eliminamos duplicados
        links_validos = list(set(links_validos))
        
        if not links_validos:
            return None

        # 2. Elegimos uno al azar
        url_producto = random.choice(links_validos)
        
        # 3. Entramos al producto para sacar el NOMBRE y la IMAGEN REAL
        res_prod = requests.get(url_producto, headers=headers, timeout=10)
        soup_prod = BeautifulSoup(res_prod.text, 'html.parser')
        
        # Intentamos sacar el nombre desde el meta tag (es lo más fiable)
        nombre_tag = soup_prod.find('meta', property="og:title")
        nombre = nombre_tag['content'].split('|')[0].strip() if nombre_tag else "Producto DarpePro"
        
        # Intentamos sacar la imagen real
        img_tag = soup_prod.find('meta', property="og:image")
        img_url = img_tag['content'] if img_tag else ""

        return {
            "nombre": nombre,
            "url": url_producto, # ESTE ES EL ENLACE DIRECTO
            "imagen_real": img_url
        }
    except Exception as e:
        print(f"Error en scraper: {e}")
        return None
