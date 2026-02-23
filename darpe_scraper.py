import requests
import random

def obtener_producto_aleatorio_total():
    # Usamos el endpoint de búsqueda predictiva de Shopify, es más estable que scrapear el HTML
    search_url = "https://darpepro.com/search/suggest.json?q=*&resources[type]=product"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.get(search_url, headers=headers, timeout=15)
        data = response.json()
        
        # Extraemos la lista de productos
        productos = data.get('resources', {}).get('results', {}).get('products', [])
        
        if not productos:
            return None

        # Elegimos uno al azar
        p = random.choice(productos)
        
        # Construimos el objeto con los datos exactos
        return {
            "nombre": p['title'].strip(),
            "url": "https://darpepro.com" + p['url'], # ENLACE DIRECTO GARANTIZADO
            "imagen_real": "https:" + p['image'] if p['image'].startswith('//') else p['image']
        }
    except Exception as e:
        print(f"Error de conexión API: {e}")
        return None
