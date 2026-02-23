import streamlit as st
import requests
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

def aplicar_plantilla_y_texto(url_ia, info_producto, frase_ia):
    try:
        # CARGA DE PLANTILLA (Asegúrate de que el nombre coincida)
        plantilla_nombre = "Plantilla DarpePRO.jpeg"
        plantilla = Image.open(plantilla_nombre).convert("RGBA")
        
        # Descargar imagen IA
        res = requests.get(url_ia)
        img_ia = Image.open(BytesIO(res.content)).convert("RGBA")
        
        # Redimensionar y pegar imagen IA
        img_ia = img_ia.resize((850, 850), Image.LANCZOS)
        plantilla.paste(img_ia, (115, 480), img_ia)
        
        # Añadir textos
        draw = ImageDraw.Draw(plantilla)
        try:
            # En Streamlit Cloud a veces hay que usar fuentes genéricas
            font_nombre = ImageFont.load_default() 
            font_frase = ImageFont.load_default()
        except:
            font_nombre = ImageFont.load_default()
            font_frase = ImageFont.load_default()

        # Dibujar nombre y frase
        draw.text((540, 1420), info_producto['nombre'].upper(), font=font_nombre, fill="white", anchor="mm")
        draw.text((540, 1500), frase_ia, font=font_frase, fill="#CCCCCC", anchor="mm")

        # Subir a ImgBB
        buffer = BytesIO()
        plantilla.convert("RGB").save(buffer, format="JPEG")
        api_key = st.secrets["IMGBB_API_KEY"]
        files = {"image": ("post_final.jpg", buffer.getvalue())}
        res_imgbb = requests.post(f"https://api.imgbb.com/1/upload?key={api_key}", files=files)
        return res_imgbb.json()["data"]["url"]
        
    except Exception as e:
        st.error(f"Error editando imagen: {e}")
        return None
