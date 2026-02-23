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
        
        # Filtramos enlaces que contengan '/products/'
        productos = [a['href'] for a in soup.find_all('a', href=True) if "/products/" in a['href']]
        productos = list(set(productos)) # Eliminar duplicados
        
        if not productos:
            return {"nombre": "Gadget Pro", "url": base_url}

        link_final = random.choice(productos)
        url_completa = base_url + link_final if link_final.startswith('/') else link_final
        nombre_limpio = link_final.split('/')[-1].replace('-', ' ').title()
        
        return {"nombre": nombre_limpio, "url": url_completa}
    except:
        return {"nombre": "Producto DarpePro", "url": base_url}
