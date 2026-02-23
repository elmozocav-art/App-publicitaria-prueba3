import streamlit as st
import requests
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont, ImageChops, ImageOps

def aplicar_plantilla_y_texto(url_ia, info_producto, frase_ia):
    try:
        # 1. Cargar imagen IA (Limpia)
        res = requests.get(url_ia)
        img_ia = Image.open(BytesIO(res.content)).convert("RGB")
        
        # 2. Cargar Plantilla DarpePRO
        plantilla = Image.open("Plantilla DarpePRO.jpeg").convert("RGB")
        ancho_p, alto_p = plantilla.size
        
        # 3. FUSIÓN: IA de fondo y Plantilla encima (Elimina el blanco)
        fondo_ia = ImageOps.fit(img_ia, (ancho_p, alto_p), Image.LANCZOS)
        imagen_final = ImageChops.multiply(fondo_ia, plantilla)
        
        # 4. TEXTO: Escribir el nombre real del producto (NO 'PRODUCTO')
        draw = ImageDraw.Draw(imagen_final)
        try:
            # Ruta de fuente para Streamlit Cloud
            font_path = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
            font_nombre = ImageFont.truetype(font_path, 65)
            font_sub = ImageFont.truetype(font_path, 40)
        except:
            font_nombre = ImageFont.load_default()
            font_sub = ImageFont.load_default()

        # Nombre del producto centrado abajo
        nombre_texto = info_producto['nombre'].upper()
        draw.text((ancho_p//2, alto_p - 450), nombre_texto, font=font_nombre, fill="white", anchor="mm")
        
        # Frase publicitaria
        draw.text((ancho_p//2, alto_p - 370), frase_ia, font=font_sub, fill="#EEEEEE", anchor="mm")

        # 5. GUARDAR Y SUBIR
        buffer = BytesIO()
        imagen_final.save(buffer, format="JPEG", quality=95)
        
        api_key = st.secrets["IMGBB_API_KEY"]
        files = {"image": ("post_darpe.jpg", buffer.getvalue())}
        res_imgbb = requests.post(f"https://api.imgbb.com/1/upload?key={api_key}", files=files)
        
        return res_imgbb.json()["data"]["url"]
        
    except Exception as e:
        st.error(f"Error editando: {e}")
        return None
