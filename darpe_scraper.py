import requests
from bs4 import BeautifulSoup
import random

def obtener_producto_aleatorio_total():
    base_url = "https://darpepro.com"
    collections_url = f"{base_url}/collections/all"
    
    # Este 'disfraz' es vital para que la web no te bloquee
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "es-ES,es;q=0.9"
    }
    
    try:
        response = requests.get(collections_url, headers=headers, timeout=15)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Buscamos todos los enlaces de la página
        enlaces = soup.find_all('a', href=True)
        links_productos = []
        
        for a in enlaces:
            href = a['href']
            # Filtramos para que solo sean productos reales
            if "/products/" in href and not any(x in href for x in ["collections", "apple-pay", "cart"]):
                full_url = href if href.startswith('http') else base_url + href
                links_productos.append(full_url)
        
        # Limpiar duplicados
        links_productos = list(set(links_productos))
        
        if not links_productos:
            return None # Si no hay links, devolvemos None para que el Main lo maneje

        # Elegimos uno y extraemos sus datos reales
        url_final = random.choice(links_productos)
        res_prod = requests.get(url_final, headers=headers, timeout=15)
        soup_prod = BeautifulSoup(res_prod.text, 'html.parser')
        
        # Título del producto
        nombre = "Producto DarpePro"
        if soup_prod.find('meta', property="og:title"):
            nombre = soup_prod.find('meta', property="og:title")['content'].split('|')[0].strip()
        elif soup_prod.h1:
            nombre = soup_prod.h1.get_text().strip()

        # Imagen real
        img_real = ""
        if soup_prod.find('meta', property="og:image"):
            img_real = soup_prod.find('meta', property="og:image")['content']

        return {
            "nombre": nombre,
            "url": url_final, # ENLACE DIRECTO COMPROBADO
            "imagen_real": img_real
        }
    except Exception as e:
        return None
