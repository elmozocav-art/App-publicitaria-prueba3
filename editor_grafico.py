from PIL import Image, ImageDraw, ImageFont, ImageChops, ImageOps
import requests
from io import BytesIO

def aplicar_plantilla_y_texto(url_ia, info_producto, frase_ia):
    try:
        res = requests.get(url_ia)
        img_ia = Image.open(BytesIO(res.content)).convert("RGB")
        plantilla = Image.open("Plantilla DarpePRO.jpeg").convert("RGB")
        
        ancho, alto = plantilla.size
        fondo = ImageOps.fit(img_ia, (ancho, alto), Image.LANCZOS)
        
        # Fusión Multiply: El blanco de tu plantilla desaparece, los logos se quedan
        imagen_final = ImageChops.multiply(fondo, plantilla)
        
        # ESCRIBIR NOMBRE REAL
        draw = ImageDraw.Draw(imagen_final)
        try:
            # Ruta estándar en servidores Linux/Streamlit
            font = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf", 65)
        except:
            font = ImageFont.load_default()

        # Forzamos el nombre que vino de la API (info_producto['nombre'])
        draw.text((ancho//2, alto - 450), info_producto['nombre'].upper(), font=font, fill="white", anchor="mm")
        
        # Guardado y subida a ImgBB...
        buffer = BytesIO()
        imagen_final.save(buffer, format="JPEG", quality=95)
        # return url_imgbb 
    except:
        return None
