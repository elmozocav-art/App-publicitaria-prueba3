import requests
from bs4 import BeautifulSoup
import random

def obtener_producto_aleatorio_total():
    base_url = "https://darpepro.com"
    # Listado completo de las 12 categorías de tu imagen
    categorias = [
        "/collections/textil", "/collections/bolsas", "/collections/tazas-y-termos",
        "/collections/oficina", "/collections/ocio", "/collections/herramientas",
        "/collections/infantil", "/collections/productos-eco", "/collections/eventos",
        "/collections/deporte", "/collections/lamina-solar", "/collections/tecnologia"
    ]
    
    url_cat = base_url + random.choice(categorias)
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        # Petición única y rápida para evitar el "Fallo de conexión"
        res = requests.get(url_cat, headers=headers, timeout=10)
        if res.status_code != 200: return None
        
        soup = BeautifulSoup(res.text, 'html.parser')
        enlaces = [a['href'] for a in soup.find_all('a', href=True) if "/products/" in a['href']]
        
        if enlaces:
            # Seleccionamos producto y construimos URL
            path_prod = random.choice(list(set(enlaces)))
            url_final = base_url + path_prod if not path_prod.startswith('http') else path_prod
            
            # Extraemos el nombre directamente de la URL para máxima velocidad y evitar bloqueos
            nombre_limpio = path_prod.split('/')[-1].replace('-', ' ').title()
            
            return {
                "nombre": nombre_limpio,
                "url": url_final
            }
    except Exception:
        return None
    return None
