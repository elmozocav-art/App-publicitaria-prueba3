import requests
from bs4 import BeautifulSoup
import random
import time

def obtener_producto_aleatorio_total():
    base_url = "https://darpepro.com"
    # Las 12 categorías exactas de tu imagen
    categorias = [
        "/collections/textil", "/collections/bolsas", "/collections/tazas-y-termos",
        "/collections/oficina", "/collections/ocio", "/collections/herramientas",
        "/collections/infantil", "/collections/productos-eco", "/collections/eventos",
        "/collections/deporte", "/collections/lamina-solar", "/collections/tecnologia"
    ]
    
    # Elegimos una al azar para empezar
    cat_path = random.choice(categorias)
    url_final = base_url + cat_path
    
    # Este 'disfraz' es vital para evitar el 'Fallo de conexión'
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "Accept-Language": "es-ES,es;q=0.9",
        "Referer": "https://google.com"
    }

    try:
        # Hacemos la petición con un pequeño retraso para no parecer un robot
        time.sleep(1)
        res = requests.get(url_final, headers=headers, timeout=15)
        
        if res.status_code != 200:
            return None

        soup = BeautifulSoup(res.text, 'html.parser')
        
        # Buscamos enlaces de productos
        enlaces = [a['href'] for a in soup.find_all('a', href=True) if "/products/" in a['href']]
        
        if not enlaces:
            return None

        # Escogemos un producto y extraemos su nombre real
        prod_link = base_url + random.choice(list(set(enlaces)))
        res_p = requests.get(prod_link, headers=headers, timeout=10)
        soup_p = BeautifulSoup(res_p.text, 'html.parser')
        
        # Sacamos el nombre real para que el Editor lo use luego
        nombre_meta = soup_p.find('meta', property="og:title")
        nombre_real = nombre_meta['content'].split('|')[0].strip() if nombre_meta else "Producto DarpePro"
        
        return {"nombre": nombre_real, "url": prod_link}
    except Exception as e:
        print(f"Error de red: {e}")
        return None
