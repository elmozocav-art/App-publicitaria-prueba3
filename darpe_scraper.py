import requests
from bs4 import BeautifulSoup
import random

def obtener_producto_aleatorio_total():
    base_url = "https://darpepro.com"
    # Volvemos a la URL más estable que no saturaba la conexión
    url_objetivo = f"{base_url}/collections/all"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        # Petición rápida con tiempo de espera corto
        res = requests.get(url_objetivo, headers=headers, timeout=5)
        soup = BeautifulSoup(res.text, 'html.parser')
        
        # Buscamos enlaces de productos
        enlaces = [a['href'] for a in soup.find_all('a', href=True) if "/products/" in a['href']]
        
        if enlaces:
            link_relativo = random.choice(list(set(enlaces)))
            url_final = base_url + link_relativo
            
            # Sacamos el nombre directamente del link para evitar una segunda carga
            nombre_limpio = link_relativo.split('/')[-1].replace('-', ' ').upper()
            
            return {
                "nombre": nombre_limpio,
                "url": url_final
            }
    except:
        return None
    return None
