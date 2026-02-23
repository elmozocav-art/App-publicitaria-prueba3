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
    
    cat_elegida = base_url + random.choice(categorias)
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    
    try:
        # Entramos a una categoría específica (más estable que /all)
        response = requests.get(cat_elegida, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Buscamos productos reales
        enlaces = [a['href'] for a in soup.find_all('a', href=True) if "/products/" in a['href']]
        
        if not enlaces: return None

        url_final = base_url + random.choice(list(set(enlaces)))
        
        # Sacamos el nombre real para evitar que la IA invente texto
        res_prod = requests.get(url_final, headers=headers)
        soup_prod = BeautifulSoup(res_prod.text, 'html.parser')
        nombre = soup_prod.find('meta', property="og:title")['content'].split('|')[0].strip()
        img_real = soup_prod.find('meta', property="og:image")['content'] if soup_prod.find('meta', property="og:image") else ""

        return {"nombre": nombre, "url": url_final, "imagen_real": img_real}
    except:
        return None
