import streamlit as st
import requests
import base64
import qrcode
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont, ImageChops, ImageOps

def procesar_imagen_auto(dato_ia, info_producto, frase_ia):
    try:
        # A. Detectar y obtener la imagen (URL o Base64)
        if str(dato_ia).startswith('http'):
            # Es una URL
            res = requests.get(dato_ia, timeout=15)
            img_ia = Image.open(BytesIO(res.content)).convert("RGB")
        else:
            # Es Base64 (Desencriptación automática)
            img_data = base64.b64decode(dato_ia)
            img_ia = Image.open(BytesIO(img_data)).convert("RGB")
        
        # B. Cargar Plantilla
        plantilla = Image.open("Plantilla DarpePRO.jpeg").convert("RGB")
        ancho, alto = plantilla.size
        
        # C. Mezclar Imagen e IA
        fondo_ia = ImageOps.fit(img_ia, (ancho, alto), Image.LANCZOS)
        imagen_final = ImageChops.multiply(fondo_ia, plantilla)
        
        # D. Generar QR del producto (Tu nuevo método de enlace)
        qr = qrcode.make(info_producto.get('url', 'https://darpepro.com')).convert('RGB').resize((150, 150))
        imagen_final.paste(qr, (ancho - 180, alto - 180))
        
        # E. Textos
        draw = ImageDraw.Draw(imagen_final)
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf", 60)
        except:
            font = ImageFont.load_default()

        draw.text((ancho // 2, alto - 300), info_producto['nombre'].upper(), font=font, fill="white", anchor="mm")
        draw.text((ancho // 2, alto - 230), frase_ia, font=font, fill="#FFD700", anchor="mm")

        # F. Subir a IMGBB
        buf = BytesIO()
        imagen_final.save(buf, format="JPEG")
        buf.seek(0)
        r = requests.post(f"https://api.imgbb.com/1/upload?key={st.secrets['IMGBB_API_KEY']}", files={"image": buf})
        return r.json()["data"]["url"]

    except Exception as e:
        st.error(f"Error en editor: {e}")
        return None
