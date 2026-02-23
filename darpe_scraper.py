import requests
from bs4 import BeautifulSoup
import random

def obtener_producto_aleatorio_total():
    base_url = "https://darpepro.com"
    # Mapeo completo de las 12 categorías de tu panel
    categorias = [
        "/collections/textil", "/collections/bolsas", "/collections/tazas-y-termos",
        "/collections/oficina", "/collections/ocio", "/collections/herramientas",
        "/collections/infantil", "/collections/productos-eco", "/collections/eventos",
        "/collections/deporte", "/collections/lamina-solar", "/collections/tecnologia"
    ]
    
    cat_elegida = base_url + random.choice(categorias)
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

    try:
        # Buscamos productos en la categoría
        res = requests.get(cat_elegida, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        links = [a['href'] for a in soup.find_all('a', href=True) if "/products/" in a['href']]
        
        if links:
            url_final = base_url + random.choice(list(set(links)))
            # Extraemos el nombre real para que Python lo escriba después
            res_p = requests.get(url_final, headers=headers)
            soup_p = BeautifulSoup(res_p.text, 'html.parser')
            nombre = soup_p.find('meta', property="og:title")['content'].split('|')[0].strip()
            
            return {"nombre": nombre, "url": url_final}
    except:
        return None
