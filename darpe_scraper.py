import requests
from bs4 import BeautifulSoup
import random

def obtener_producto_aleatorio_total():
    base_url = "https://darpepro.com"
    collections_url = f"{base_url}/collections/all"
    
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(collections_url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Filtramos para obtener solo enlaces de productos individuales
        productos = [a['href'] for a in soup.find_all('a', href=True) if "/products/" in a['href']]
        productos = list(set(productos)) # Eliminar duplicados
        
        if not productos:
            return {"nombre": "Producto DarpePro", "url": base_url}

        # Elegimos uno al azar
        link_relativo = random.choice(productos)
        
        # CONSTRUCCIÓN DEL ENLACE DIRECTO
        url_directa = base_url + link_relativo if link_relativo.startswith('/') else link_relativo
        
        # Limpiamos el nombre para que quede profesional
        nombre_limpio = link_relativo.split('/')[-1].replace('-', ' ').title()
        
        return {
            "nombre": nombre_limpio,
            "url": url_directa # Esta es la URL que usaremos en Instagram
        }
    except Exception as e:
        return {"nombre": "Producto DarpePro", "url": base_url}
