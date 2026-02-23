import streamlit as st
import requests
import base64
from io import BytesIO
from PIL import Image

def aplicar_marca_agua(url_imagen_ia, ruta_logo="logoDarpe.png"):
    try:
        # 1. Descargar imagen de la IA
        res = requests.get(url_imagen_ia)
        img = Image.open(BytesIO(res.content)).convert("RGBA")
        
        # 2. Cargar y redimensionar logo
        logo = Image.open(ruta_logo).convert("RGBA")
        ancho_logo = int(img.width * 0.2)
        alto_logo = int(logo.height * (ancho_logo / logo.width))
        logo = logo.resize((ancho_logo, alto_logo), Image.LANCZOS)
        
        # 3. Posición y pegado
        pos = (img.width - ancho_logo - 20, img.height - alto_logo - 20)
        img.paste(logo, pos, logo)
        
        # 4. Guardar en memoria (sin archivos locales estorbando)
        buffer = BytesIO()
        img.convert("RGB").save(buffer, format="JPEG")
        buffer.seek(0)

        # 5. SUBIDA AUTOMÁTICA A IMGBB
        api_key = st.secrets["IMGBB_API_KEY"] # Aquí lee lo que pusiste en Secrets
        url_upload = "https://api.imgbb.com/1/upload"
        
        files = {"image": ("post_final.jpg", buffer.getvalue())}
        params = {"key": api_key}
        
        respuesta = requests.post(url_upload, params=params, files=files)
        datos = respuesta.json()
        
        # DEVOLVEMOS LA URL PÚBLICA (Termina en .jpg)
        return datos["data"]["url"] 
        
    except Exception as e:
        st.error(f"Error en edición/subida: {e}")
        return None
