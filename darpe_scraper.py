import requests
from bs4 import BeautifulSoup
import random

def obtener_producto_aleatorio_total():
    base_url = "https://darpepro.com"
    collections_url = f"{base_url}/collections/all"
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(collections_url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Buscamos todos los bloques de producto
        items = soup.find_all('div', class_='grid-view-item') or soup.find_all('a', href=True)
        
        enlaces_validos = []
        for a in soup.find_all('a', href=True):
            if "/products/" in a['href']:
                enlaces_validos.append(a['href'])
        
        link_final = random.choice(list(set(enlaces_validos)))
        url_producto = base_url + link_final if link_final.startswith('/') else link_final
        
        # Entramos al producto para sacar su FOTO REAL
        res_prod = requests.get(url_producto, headers=headers)
        soup_prod = BeautifulSoup(res_prod.text, 'html.parser')
        img_tag = soup_prod.find('meta', property="og:image")
        img_real = img_tag['content'] if img_tag else ""

        nombre = link_final.split('/')[-1].replace('-', ' ').title()
        
        return {"nombre": nombre, "url": url_producto, "imagen_real": img_real}
    except:
        return {"nombre": "Producto", "url": base_url, "imagen_real": ""}
