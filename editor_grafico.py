from PIL import Image, ImageDraw, ImageFont, ImageChops, ImageOps
import requests
from io import BytesIO

def aplicar_plantilla_y_texto(url_ia, info_producto, frase_ia):
    # 1. Cargar imágenes
    res = requests.get(url_ia)
    img_ia = Image.open(BytesIO(res.content)).convert("RGB")
    plantilla = Image.open("Plantilla DarpePRO.jpeg").convert("RGB")
    
    # 2. Ajustar fondo al tamaño de la plantilla
    ancho_p, alto_p = plantilla.size
    fondo = ImageOps.fit(img_ia, (ancho_p, alto_p), Image.LANCZOS)
    
    # 3. Fusión Multiply (Quita el blanco)
    imagen_final = ImageChops.multiply(fondo, plantilla)
    
    # 4. Escribir el NOMBRE REAL del producto (Sacado del Scraper)
    draw = ImageDraw.Draw(imagen_final)
    try:
        # Intenta cargar la fuente de sistema en Streamlit Cloud
        font = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf", 65)
    except:
        font = ImageFont.load_default()

    # Escribir el nombre en mayúsculas
    nombre_a_escribir = info_producto['nombre'].upper()
    draw.text((ancho_p//2, alto_p - 450), nombre_a_escribir, font=font, fill="white", anchor="mm")
    
    # 5. Guardar y subir a ImgBB
    buffer = BytesIO()
    imagen_final.save(buffer, format="JPEG", quality=95)
    # ... (Aquí va tu lógica de subida a ImgBB) ...
    return url_imgbb # Retorna la URL de ImgBB
