from PIL import Image, ImageChops, ImageOps, ImageDraw, ImageFont
import requests
from io import BytesIO
import streamlit as st

def aplicar_plantilla_y_texto(url_ia, info_producto, frase_ia):
    try:
        res = requests.get(url_ia)
        img_ia = Image.open(BytesIO(res.content)).convert("RGB")
        plantilla = Image.open("Plantilla DarpePRO.jpeg").convert("RGB")
        
        # Ajustar tamaño
        fondo = ImageOps.fit(img_ia, plantilla.size, Image.LANCZOS)
        
        # Combinar (Multiply quita el blanco de la plantilla)
        final = ImageChops.multiply(fondo, plantilla)
        
        # Escribir nombre
        draw = ImageDraw.Draw(final)
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf", 60)
        except:
            font = ImageFont.load_default()
            
        draw.text((plantilla.size[0]//2, plantilla.size[1]-450), info_producto['nombre'].upper(), font=font, fill="white", anchor="mm")
        
        # Subir a ImgBB
        buffer = BytesIO()
        final.save(buffer, format="JPEG")
        files = {"image": ("post.jpg", buffer.getvalue())}
        res_imgbb = requests.post(f"https://api.imgbb.com/1/upload?key={st.secrets['IMGBB_API_KEY']}", files=files)
        return res_imgbb.json()["data"]["url"]
    except:
        return None
