import streamlit as st
import requests
import base64
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont, ImageChops, ImageOps

def aplicar_plantilla_y_texto_base64(img_base64, info_producto, frase_ia):
    try:
        # 1️⃣ Decodificar Base64 (Lo que el video enseña a hacer)
        img_data = base64.b64decode(img_base64)
        img_ia = Image.open(BytesIO(img_data)).convert("RGB")
        
        # 2️⃣ Cargar plantilla
        plantilla = Image.open("Plantilla DarpePRO.jpeg").convert("RGB")
        ancho_p, alto_p = plantilla.size
        
        # 3️⃣ Ajustar y Mezclar
        fondo_ia = ImageOps.fit(img_ia, (ancho_p, alto_p), Image.LANCZOS)
        imagen_final = ImageChops.multiply(fondo_ia, plantilla)
        
        draw = ImageDraw.Draw(imagen_final)

        # 4️⃣ Textos
        font_path = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
        try:
            font_nombre = ImageFont.truetype(font_path, 80)
        except:
            font_nombre = ImageFont.load_default()

        y_base = alto_p - 480
        nombre_prod = info_producto.get('nombre', 'DarpePro').upper()
        draw.text((ancho_p // 2, y_base), nombre_prod, font=font_nombre, fill="white", anchor="mm")

        # 5️⃣ Guardar y subir
        buffer = BytesIO()
        imagen_final.save(buffer, format="JPEG", quality=95)
        buffer.seek(0)

        api_key = st.secrets["IMGBB_API_KEY"]
        files = {"image": ("post.jpg", buffer)}
        res_imgbb = requests.post(f"https://api.imgbb.com/1/upload?key={api_key}", files=files)
        
        return res_imgbb.json()["data"]["url"]

    except Exception as e:
        st.error(f"⚠️ Error en editor: {e}")
        return None
