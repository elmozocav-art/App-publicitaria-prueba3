import requests
from bs4 import BeautifulSoup
import random

def obtener_producto_aleatorio_total():
    base_url = "https://darpepro.com"
    # Mapeo completo de las 12 secciones de tu imagen
    categorias = [
        "/collections/textil", "/collections/bolsas", "/collections/tazas-y-termos",
        "/collections/oficina", "/collections/ocio", "/collections/herramientas",
        "/collections/infantil", "/collections/productos-eco", "/collections/eventos",
        "/collections/deporte", "/collections/lamina-solar", "/collections/tecnologia"
    ]
    
    random.shuffle(categorias) # Mezclamos para variar el contenido
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

    for cat in categorias:
        try:
            url_cat = base_url + cat
            res = requests.get(url_cat, headers=headers, timeout=10)
            if res.status_code != 200: continue
            
            soup = BeautifulSoup(res.text, 'html.parser')
            # Buscamos enlaces de productos (excluyendo colecciones)
            links = [a['href'] for a in soup.find_all('a', href=True) 
                     if "/products/" in a['href'] and "collections" not in a['href']]
            
            if links:
                url_prod = base_url + random.choice(list(set(links)))
                # Entramos al producto para sacar el nombre real
                res_p = requests.get(url_prod, headers=headers, timeout=10)
                soup_p = BeautifulSoup(res_p.text, 'html.parser')
                nombre = soup_p.find('meta', property="og:title")['content'].split('|')[0].strip()
                
                return {"nombre": nombre, "url": url_prod}
        except:
            continue # Si esta categoría falla, prueba la siguiente
            
    return None
