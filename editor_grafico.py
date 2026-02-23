import streamlit as st
import requests
import base64
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

def aplicar_plantilla_y_texto(url_ia, info_producto, frase_ia):
    try:
        # 1. Cargar Plantilla y descargar imagen IA
        plantilla = Image.open("Plantilla DarpePRO.jpeg").convert("RGBA")
        res = requests.get(url_ia)
        img_ia = Image.open(BytesIO(res.content)).convert("RGBA")
        
        # 2. Redimensionar imagen IA para el centro del Reel
        img_ia = img_ia.resize((850, 850), Image.LANCZOS)
        plantilla.paste(img_ia, (115, 480), img_ia) # Posición central aproximada
        
        # 3. Dibujar textos
        draw = ImageDraw.Draw(plantilla)
        # Nota: Asegúrate de tener una fuente .ttf en tu carpeta o usa la de defecto
        try:
            font_nombre = ImageFont.truetype("Arial-Bold.ttf", 70)
            font_frase = ImageFont.truetype("Arial.ttf", 40)
        except:
            font_nombre = ImageFont.load_default()
            font_frase = ImageFont.load_default()

        # Nombre del producto (arriba de la URL de la plantilla)
        draw.text((540, 1420), info_producto['nombre'].upper(), font=font_nombre, fill="white", anchor="mm")
        # Frase generada por IA
        draw.text((540, 1500), frase_ia, font=font_frase, fill="#CCCCCC", anchor="mm")

        # 4. Guardar y subir a ImgBB
        buffer = BytesIO()
        plantilla.convert("RGB").save(buffer, format="JPEG")
        
        api_key = st.secrets["IMGBB_API_KEY"]
        files = {"image": ("reel_final.jpg", buffer.getvalue())}
        res_imgbb = requests.post(f"https://api.imgbb.com/1/upload?key={api_key}", files=files)
        return res_imgbb.json()["data"]["url"]
        
    except Exception as e:
        st.error(f"Error editando imagen: {e}")
        return None
