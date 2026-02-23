import requests
from bs4 import BeautifulSoup
import random

def obtener_producto_aleatorio_total():
    base_url = "https://darpepro.com"
    # Las 12 categorías exactas de tu imagen
    categorias = [
        "/collections/textil", "/collections/bolsas", "/collections/tazas-y-termos",
        "/collections/oficina", "/collections/ocio", "/collections/herramientas",
        "/collections/infantil", "/collections/productos-eco", "/collections/eventos",
        "/collections/deporte", "/collections/lamina-solar", "/collections/tecnologia"
    ]
    
    url_cat = base_url + random.choice(categorias)
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        # Petición simple para evitar bloqueos
        res = requests.get(url_cat, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        
        # Buscamos enlaces de productos
        enlaces = [a['href'] for a in soup.find_all('a', href=True) if "/products/" in a['href']]
        
        if enlaces:
            url_prod = base_url + random.choice(list(set(enlaces)))
            # Sacamos el nombre directamente de la URL para no hacer otra petición y evitar fallos
            nombre = url_prod.split('/')[-1].replace('-', ' ').title()
            
            return {"nombre": nombre, "url": url_prod}
    except:
        return None
    return None
