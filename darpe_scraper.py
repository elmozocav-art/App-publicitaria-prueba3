import requests
from bs4 import BeautifulSoup
import random

def obtener_producto_aleatorio_total():
    base_url = "https://darpepro.com"
    
    # Lista completa y exacta de las 12 categorías de tu imagen
    categorias = [
        "/collections/textil",           # Icono 1: Camiseta
        "/collections/bolsas",           # Icono 2: Bolsa
        "/collections/tazas-y-termos",   # Icono 3: Taza
        "/collections/oficina",          # Icono 4: Escritorio
        "/collections/ocio",             # Icono 5: Dado
        "/collections/herramientas",     # Icono 6: Herramientas
        "/collections/infantil",         # Icono 7: Bebé
        "/collections/productos-eco",    # Icono 8: Reciclaje
        "/collections/eventos",          # Icono 9: Fiesta
        "/collections/deporte",          # Icono 10: Baloncesto
        "/collections/lamina-solar",     # Icono 11: Coche/Sol
        "/collections/tecnologia"        # Icono 12: Portátil
    ]
    
    # Elegimos una de las 12 al azar
    categoria_elegida = random.choice(categorias)
    url_categoria = base_url + categoria_elegida
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    try:
        # 1. Entramos en la categoría
        res = requests.get(url_categoria, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        
        # 2. Capturamos todos los enlaces de productos (/products/)
        # Filtramos para que no se confunda con enlaces de colecciones o legales
        enlaces = [a['href'] for a in soup.find_all('a', href=True) 
                  if "/products/" in a['href'] and "collections" not in a['href']]
        
        if not enlaces:
            return None

        # 3. Elegimos un producto al azar y construimos su URL completa
        link_relativo = random.choice(list(set(enlaces)))
        url_producto_directa = base_url + link_relativo
        
        # 4. Entramos al producto para sacar el NOMBRE REAL (para evitar el texto 'PRODUCTO')
        res_p = requests.get(url_producto_directa, headers=headers, timeout=10)
        soup_p = BeautifulSoup(res_p.text, 'html.parser')
        
        # El nombre suele estar en el meta tag 'og:title' o en el <h1>
        nombre_tag = soup_p.find('meta', property="og:title")
        nombre_real = nombre_tag['content'].split('|')[0].strip() if nombre_tag else "Producto DarpePro"
        
        return {
            "nombre": nombre_real,
            "url": url_producto_directa # ENLACE DIRECTO GARANTIZADO
        }
        
    except Exception as e:
        print(f"Error en scraper: {e}")
        return None
