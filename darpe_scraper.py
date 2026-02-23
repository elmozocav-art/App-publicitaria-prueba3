import requests
from bs4 import BeautifulSoup
import random

def obtener_producto_aleatorio_total():
    base_url = "https://darpepro.com"
    # Usamos la ruta más genérica y estable
    url_objetivo = f"{base_url}/collections/all"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        # Petición directa con un timeout corto para evitar bloqueos prolongados
        res = requests.get(url_objetivo, headers=headers, timeout=5)
        if res.status_code != 200:
            return None
            
        soup = BeautifulSoup(res.text, 'html.parser')
        
        # Extraemos enlaces de productos (sin navegar por categorías)
        enlaces = [a['href'] for a in soup.find_all('a', href=True) if "/products/" in a['href']]
        
        if enlaces:
            path_producto = random.choice(list(set(enlaces)))
            url_final = base_url + path_producto if not path_producto.startswith('http') else path_producto
            
            # Generamos el nombre directamente desde el texto del link para no cargar la web otra vez
            nombre_producto = path_producto.split('/')[-1].replace('-', ' ').upper()
            
            return {
                "nombre": nombre_producto,
                "url": url_final
            }
    except Exception:
        return None
    return None
