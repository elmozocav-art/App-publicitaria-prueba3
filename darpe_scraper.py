import requests
from bs4 import BeautifulSoup
import random

def obtener_producto_aleatorio_total():
    base_url = "https://darpepro.com"
    # Las 12 categorías mapeadas según tu imagen
    categorias = [
        f"{base_url}/collections/textil",       # Textil
        f"{base_url}/collections/bolsas",       # Bolsas
        f"{base_url}/collections/tazas-y-termos", # Tazas y termos
        f"{base_url}/collections/oficina",      # Oficina
        f"{base_url}/collections/ocio",         # Ocio
        f"{base_url}/collections/herramientas", # Herramientas
        f"{base_url}/collections/infantil",     # Infantil
        f"{base_url}/collections/productos-eco", # Productos Eco
        f"{base_url}/collections/eventos",       # Eventos
        f"{base_url}/collections/deporte",       # Deporte
        f"{base_url}/collections/lamina-solar",  # Lamina solar
        f"{base_url}/collections/tecnologia"     # Tecnología
    ]
    
    url_categoria = random.choice(categorias)
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    
    try:
        response = requests.get(url_categoria, headers=headers, timeout=12)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extraemos los enlaces de productos reales
        enlaces = soup.find_all('a', href=True)
        links_directos = []
        
        for a in enlaces:
            href = a['href']
            # Filtramos para que sea un producto individual y no una sub-colección
            if "/products/" in href and "collections" not in href:
                full_url = href if href.startswith('http') else base_url + href
                links_directos.append(full_url)
        
        if not links_directos:
            return None # Si la categoría está vacía, el Main reintentará

        # Elegimos un producto al azar de la lista
        url_final = random.choice(list(set(links_directos)))
        
        # Entramos al producto para obtener el nombre real (Evita el texto 'PRODUCTO')
        res_prod = requests.get(url_final, headers=headers)
        soup_prod = BeautifulSoup(res_prod.text, 'html.parser')
        
        nombre_meta = soup_prod.find('meta', property="og:title")
        nombre_real = nombre_meta['content'].split('|')[0].strip() if nombre_meta else "Producto DarpePro"
        
        return {
            "nombre": nombre_real,
            "url": url_final # ENLACE DIRECTO GARANTIZADO
        }
    except Exception as e:
        print(f"Error accediendo a {url_categoria}: {e}")
        return None
