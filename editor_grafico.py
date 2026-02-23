import requests
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont, ImageChops, ImageOps
import streamlit as st

def aplicar_plantilla_y_texto(url_ia, info_producto, frase_ia):
    try:
        # Cargar IA y Plantilla
        res = requests.get(url_ia)
        img_ia = Image.open(BytesIO(res.content)).convert("RGB")
        plantilla = Image.open("Plantilla DarpePRO.jpeg").convert("RGB")
        
        # Ajustar fondo
        ancho_p, alto_p = plantilla.size
        fondo = ImageOps.fit(img_ia, (ancho_p, alto_p), Image.LANCZOS)
        
        # Fusión para eliminar fondo blanco de la plantilla
        imagen_final = ImageChops.multiply(fondo, plantilla)
        
        # Dibujar nombre del producto REAL (no 'Producto')
        draw = ImageDraw.Draw(imagen_final)
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf", 60)
        except:
            font = ImageFont.load_default()
            
        draw.text((ancho_p//2, alto_p - 450), info_producto['nombre'].upper(), font=font, fill="white", anchor="mm")
        
        # Guardar y subir
        buffer = BytesIO()
        imagen_final.save(buffer, format="JPEG", quality=95)
        
        api_key = st.secrets["IMGBB_API_KEY"]
        files = {"image": ("reel.jpg", buffer.getvalue())}
        res_imgbb = requests.post(f"https://api.imgbb.com/1/upload?key={api_key}", files=files)
        return res_imgbb.json()["data"]["url"]
        
    except Exception as e:
        st.error(f"Error: {e}")
        return None
