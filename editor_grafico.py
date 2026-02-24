import streamlit as st
import requests
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont, ImageChops, ImageOps

def aplicar_plantilla_y_texto(url_ia, info_producto, frase_ia):
    # BLINDAJE: Si no hay URL, salimos antes de que explote el error 'format'
    if not url_ia:
        return None
    
    try:
        # 1️⃣ Descarga con reintentos
        res = requests.get(url_ia, timeout=15)
        img_ia = Image.open(BytesIO(res.content)).convert("RGB")
        
        # 2️⃣ Carga de plantilla
        try:
            plantilla = Image.open("Plantilla DarpePRO.jpeg").convert("RGB")
        except:
            st.error("❌ No se encontró la plantilla física.")
            return None

        ancho_p, alto_p = plantilla.size
        
        # 3️⃣ Mezcla de capas
        fondo_ia = ImageOps.fit(img_ia, (ancho_p, alto_p), Image.LANCZOS)
        imagen_final = ImageChops.multiply(fondo_ia, plantilla)
        
        draw = ImageDraw.Draw(imagen_final)

        # 4️⃣ Fuentes (con respaldo para evitar errores)
        try:
            font_path = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
            font_nombre = ImageFont.truetype(font_path, 80)
            font_frase = ImageFont.truetype(font_path, 55)
        except:
            font_nombre = font_frase = ImageFont.load_default()

        # 5️⃣ Dibujar textos con seguridad (usando .get para evitar errores de diccionario)
        y_base = alto_p - 480
        nombre_prod = info_producto.get('nombre', 'Producto DarpePro').upper()
        
        draw.text((ancho_p // 2, y_base), nombre_prod, font=font_nombre, fill="white", anchor="mm")
        draw.text((ancho_p // 2, y_base + 90), frase_ia, font=font_frase, fill="#F0F0F0", anchor="mm")

        # 6️⃣ Guardado seguro
        buffer = BytesIO()
        imagen_final.save(buffer, format="JPEG", quality=95)
        buffer.seek(0)

        # 7️⃣ Subida a IMGBB
        api_key = st.secrets["IMGBB_API_KEY"]
        files = {"image": ("reel.jpg", buffer)}
        res_imgbb = requests.post(f"https://api.imgbb.com/1/upload?key={api_key}", files=files)
        
        return res_imgbb.json()["data"]["url"]

    except Exception as e:
        st.error(f"⚠️ Error en procesamiento: {e}")
        return None
