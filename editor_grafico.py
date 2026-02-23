from PIL import Image, ImageDraw, ImageFont, ImageChops, ImageOps
import requests
from io import BytesIO

def aplicar_plantilla_y_texto(url_ia, info_producto, frase_ia):
    # 1. Obtenemos la imagen limpia de la IA
    res = requests.get(url_ia)
    img_ia = Image.open(BytesIO(res.content)).convert("RGB")
    
    # 2. Plantilla DarpePRO
    plantilla = Image.open("Plantilla DarpePRO.jpeg").convert("RGB")
    ancho_p, alto_p = plantilla.size
    
    # 3. Fusión total (IA como fondo de la plantilla)
    fondo_ia = ImageOps.fit(img_ia, (ancho_p, alto_p), Image.LANCZOS)
    imagen_final = ImageChops.multiply(fondo_ia, plantilla)
    
    # 4. ESCRIBIR EL NOMBRE REAL (Aquí es donde forzamos el nombre del scraper)
    draw = ImageDraw.Draw(imagen_final)
    try:
        font_path = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
        font_nombre = ImageFont.truetype(font_path, 60)
    except:
        font_nombre = ImageFont.load_default()

    # Escribimos el nombre REAL (info_producto['nombre']) para que nunca diga "Producto"
    # Lo centramos en la parte inferior sobre la banda de la plantilla
    nombre_real = info_producto['nombre'].upper()
    draw.text((ancho_p//2, alto_p - 450), nombre_real, font=font_nombre, fill="white", anchor="mm")
    
    # (Resto del código de guardado y subida...)
    return enviar_a_imgbb(imagen_final)
