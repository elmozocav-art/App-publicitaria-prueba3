from PIL import Image, ImageChops, ImageOps, ImageDraw, ImageFont
import requests
from io import BytesIO

def aplicar_plantilla_y_texto(url_ia, info_producto, frase_ia):
    res = requests.get(url_ia)
    img_ia = Image.open(BytesIO(res.content)).convert("RGB")
    plantilla = Image.open("Plantilla DarpePRO.jpeg").convert("RGB")
    
    # Adaptar IA al fondo
    ancho, alto = plantilla.size
    fondo = ImageOps.fit(img_ia, (ancho, alto), Image.LANCZOS)
    
    # FUSIÓN: Quita el blanco de la plantilla
    imagen_final = ImageChops.multiply(fondo, plantilla)
    
    # Escribir el nombre REAL (evita que diga 'PRODUCTO')
    draw = ImageDraw.Draw(imagen_final)
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf", 65)
    except:
        font = ImageFont.load_default()

    draw.text((ancho//2, alto - 450), info_producto['nombre'].upper(), font=font, fill="white", anchor="mm")
    
    # Guardado y subida...
    return "url_final_imgbb"
