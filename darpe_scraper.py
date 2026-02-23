import requests
from bs4 import BeautifulSoup
import random

def obtener_producto_aleatorio_total():
    base_url = "https://darpepro.com"
    # Las 12 categorías que solicitaste de tu panel
    categorias = [
        "/collections/textil", "/collections/bolsas", "/collections/tazas-y-termos",
        "/collections/oficina", "/collections/ocio", "/collections/herramientas",
        "/collections/infantil", "/collections/productos-eco", "/collections/eventos",
        "/collections/deporte", "/collections/lamina-solar", "/collections/tecnologia"
    ]
    
    url_objetivo = base_url + random.choice(categorias)
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        respuesta = requests.get(url_objetivo, headers=headers, timeout=10)
        soup = BeautifulSoup(respuesta.text, 'html.parser')
        
        # Buscamos los enlaces a productos
        enlaces = [a['href'] for a in soup.find_all('a', href=True) if "/products/" in a['href']]
        
        if enlaces:
            # Limpiamos duplicados y elegimos uno
            link_producto = random.choice(list(set(enlaces)))
            url_final = base_url + link_producto if not link_producto.startswith('http') else link_producto
            
            # Sacamos el nombre del link para que sea rápido y no falle la conexión
            nombre_sucio = link_producto.split('/')[-1].replace('-', ' ').title()
            
            return {
                "nombre": nombre_sucio,
                "url": url_final
            }
    except:
        return None
