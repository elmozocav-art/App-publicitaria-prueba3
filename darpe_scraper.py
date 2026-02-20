import requests
from bs4 import BeautifulSoup
import random

def obtener_producto_aleatorio_total():
    categorias = [
        "https://www.darpeshop.es/c105574-portatiles.html",
        "https://www.darpeshop.es/c105573-pcs-sobremesa.html",
        "https://www.darpeshop.es/c105575-monitores.html"
    ]
    url_objetivo = random.choice(categorias)
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        respuesta = requests.get(url_objetivo, headers=headers)
        soup = BeautifulSoup(respuesta.text, 'html.parser')
        # Buscamos los nombres en las etiquetas h3 según vimos en la web
        productos_html = soup.find_all(['h2', 'h3'])
        nombres = [p.get_text().strip() for p in productos_html if len(p.get_text().strip()) > 10]
        
        if nombres:
            return random.choice(nombres)
        return "Portátil HP Profesional" # Backup por si falla la lectura
    except:
        return "Producto Informático Darpe"