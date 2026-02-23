import requests
from bs4 import BeautifulSoup
import random

def obtener_producto_aleatorio_total():
    base_url = "https://darpepro.com"
    collections_url = f"{base_url}/collections/all"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        response = requests.get(collections_url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Buscamos todos los enlaces que contengan '/products/'
        enlaces = soup.find_all('a', href=True)
        links_productos = []
        
        for a in enlaces:
            href = a['href']
            if "/products/" in href and "collections" not in href:
                # Si el link es relativo, le pegamos la base
                full_url = href if href.startswith('http') else base_url + href
                links_productos.append(full_url)
        
        # Eliminamos duplicados y elegimos uno al azar
        url_final = random.choice(list(set(links_productos)))
        
        # Entramos al producto para sacar el nombre real y la imagen real
        res_prod = requests.get(url_final, headers=headers)
        soup_prod = BeautifulSoup(res_prod.text, 'html.parser')
        
        # Extraer nombre desde la etiqueta meta o el h1
        nombre = soup_prod.find('meta', property="og:title")['content'] if soup_prod.find('meta', property="og:title") else "Producto Tecnológico"
        # Extraer imagen real del producto
        img_real = soup_prod.find('meta', property="og:image")['content'] if soup_prod.find('meta', property="og:image") else ""

        return {
            "nombre": nombre.split('|')[0].strip(), # Limpiamos el nombre si trae basura
            "url": url_final, 
            "imagen_real": img_real
        }
    except Exception as e:
        return {"nombre": "Gadget Pro", "url": base_url, "imagen_real": ""}
