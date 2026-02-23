import requests
from bs4 import BeautifulSoup
import random
import time

def obtener_producto_aleatorio_total():
    base_url = "https://darpepro.com"
    # Las 12 categorías exactas de tu panel
    categorias = [
        "/collections/textil", "/collections/bolsas", "/collections/tazas-y-termos",
        "/collections/oficina", "/collections/ocio", "/collections/herramientas",
        "/collections/infantil", "/collections/productos-eco", "/collections/eventos",
        "/collections/deporte", "/collections/lamina-solar", "/collections/tecnologia"
    ]
    
    # Creamos una sesión para mantener las cookies (esto evita el error crítico)
    session = requests.Session()
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3",
        "DNT": "1"
    })

    # Intentamos hasta 3 veces con categorías diferentes si falla la conexión
    for _ in range(3):
        try:
            url_cat = base_url + random.choice(categorias)
            # Pequeña pausa para no saturar el servidor
            time.sleep(2) 
            
            res = session.get(url_cat, timeout=15)
            if res.status_code != 200:
                continue # Prueba otra categoría si esta da error

            soup = BeautifulSoup(res.text, 'html.parser')
            # Extraer enlaces de productos específicos
            enlaces = [a['href'] for a in soup.find_all('a', href=True) 
                      if "/products/" in a['href'] and "collections" not in a['href']]
            
            if enlaces:
                prod_path = random.choice(list(set(enlaces)))
                url_prod = base_url + prod_path
                
                # Segunda petición para el nombre real
                time.sleep(1)
                res_p = session.get(url_prod, timeout=10)
                soup_p = BeautifulSoup(res_p.text, 'html.parser')
                
                nombre = soup_p.find('meta', property="og:title")
                nombre_real = nombre['content'].split('|')[0].strip() if nombre else "Producto DarpePro"
                
                return {"nombre": nombre_real, "url": url_prod}
        except Exception:
            continue # Salta a la siguiente categoría si hay error de conexión

    return None

