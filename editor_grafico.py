from PIL import Image, ImageDraw, ImageFont, ImageChops, ImageOps
import requests
from io import BytesIO

def aplicar_plantilla_y_texto(url_ia, info_producto, frase_ia):
    try:
        # Cargar imágenes
        res = requests.get(url_ia)
        img_ia = Image.open(BytesIO(res.content)).convert("RGB")
        plantilla = Image.open("Plantilla DarpePRO.jpeg").convert("RGB")
        
        # Ajuste de tamaño
        ancho, alto = plantilla.size
        fondo = ImageOps.fit(img_ia, (ancho, alto), Image.LANCZOS)
        
        # Fusión Multiply para quitar el fondo blanco de la plantilla
        imagen_final = ImageChops.multiply(fondo, plantilla)
        
        # Escribir nombre real del producto
        draw = ImageDraw.Draw(imagen_final)
        try:
            # Fuente para Streamlit Cloud
            font = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf", 65)
        except:
            font = ImageFont.load_default()

        # Escribimos el nombre que el scraper trajo (info_producto['nombre'])
        draw.text((ancho//2, alto - 450), info_producto['nombre'].upper(), font=font, fill="white", anchor="mm")
        
        # Guardar y preparar para subir
        buffer = BytesIO()
        imagen_final.save(buffer, format="JPEG", quality=95)
        
        # Aquí enviarías a ImgBB...
        # return url_imgbb 
    except:
        return None
