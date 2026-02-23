import streamlit as st
import requests
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont, ImageChops, ImageOps

def aplicar_plantilla_y_texto(url_ia, info_producto, frase_ia):
    try:
        # 1. Descargar imagen de la IA
        res = requests.get(url_ia)
        img_ia = Image.open(BytesIO(res.content)).convert("RGB")
        
        # 2. Cargar tu Plantilla (la que tiene los logos y fondo blanco)
        # Debe estar en tu GitHub con este nombre exacto
        plantilla = Image.open("Plantilla DarpePRO.jpeg").convert("RGB")
        ancho_p, alto_p = plantilla.size # Tamaño original del Reel
        
        # 3. AJUSTE DE FONDO: 
        # Hacemos que la imagen de la IA rellene TODO el lienzo de la plantilla
        fondo_ia = ImageOps.fit(img_ia, (ancho_p, alto_p), Image.LANCZOS)
        
        # 4. TRUCO DE FUSIÓN (MULTIPLY):
        # Esta línea hace que el blanco de la plantilla sea transparente 
        # y los logos oscuros se mantengan sobre la foto de la IA.
        imagen_final = ImageChops.multiply(fondo_ia, plantilla)
        
        # 5. AÑADIR TEXTOS PROFESIONALES
        draw = ImageDraw.Draw(imagen_final)
        try:
            # Fuentes en Streamlit Cloud (Linux)
            font_path = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
            font_nombre = ImageFont.truetype(font_path, 65)
            font_frase = ImageFont.truetype(font_path, 40)
        except:
            font_nombre = ImageFont.load_default()
            font_frase = ImageFont.load_default()

        # Posicionamos el texto en la zona inferior, antes del link de la web
        draw.text((ancho_p//2, alto_p - 450), info_producto['nombre'].upper(), 
                  font=font_nombre, fill="white", anchor="mm")
        
        draw.text((ancho_p//2, alto_p - 370), frase_ia, 
                  font=font_frase, fill="#EEEEEE", anchor="mm")

        # 6. GUARDAR Y SUBIR A IMGBB
        buffer = BytesIO()
        imagen_final.save(buffer, format="JPEG", quality=95)
        
        api_key = st.secrets["IMGBB_API_KEY"]
        files = {"image": ("reel_final.jpg", buffer.getvalue())}
        res_imgbb = requests.post(f"https://api.imgbb.com/1/upload?key={api_key}", files=files)
        
        return res_imgbb.json()["data"]["url"]
        
    except Exception as e:
        st.error(f"Fallo en el editor: {e}")
        return None
