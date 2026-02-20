from PIL import Image
import requests
from io import BytesIO

def aplicar_marca_agua(url_imagen_ia, ruta_logo="logoDarpe.png"):
    try:
        # Descargar imagen de la IA
        res = requests.get(url_imagen_ia)
        img = Image.open(BytesIO(res.content)).convert("RGBA")
        
        # Cargar logo
        logo = Image.open("logoDarpe.png").convert("RGBA")
        
        # Redimensionar logo al 20% del ancho de la imagen
        ancho_logo = int(img.width * 0.2)
        alto_logo = int(logo.height * (ancho_logo / logo.width))
        logo = logo.resize((ancho_logo, alto_logo), Image.LANCZOS)
        
        # Posición: Esquina inferior derecha
        pos = (img.width - ancho_logo - 20, img.height - alto_logo - 20)
        
        # Pegar
        img.paste(logo, pos, logo)
        
        resultado_path = "post_final.png"
        img.convert("RGB").save(resultado_path)
        return resultado_path
    except Exception as e:
        print(f"Error editando imagen: {e}")
        return None