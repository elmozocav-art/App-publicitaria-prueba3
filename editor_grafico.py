import streamlit as st
import requests
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont, ImageChops, ImageOps

def aplicar_plantilla_y_texto(url_ia, info_producto, frase_ia):
    # BLINDAJE: Detener proceso si no hay imagen
    if not url_ia:
        return None
    
    try:
        # 1️⃣ Descarga segura con timeout
        res = requests.get(url_ia, timeout=15)
        img_ia = Image.open(BytesIO(res.content)).convert("RGB")
        
        # 2️⃣ Carga de plantilla DarpePro
        try:
            plantilla = Image.open("Plantilla DarpePRO.jpeg").convert("RGB")
        except:
            st.error("❌ Archivo 'Plantilla DarpePRO.jpeg' no encontrado.")
            return None

        ancho_p, alto_p = plantilla.size
        
        # 3️⃣ Ajustar imagen IA al tamaño de plantilla
        fondo_ia = ImageOps.fit(img_ia, (ancho_p, alto_p), Image.LANCZOS)
        imagen_final = ImageChops.multiply(fondo_ia, plantilla)
        
        draw = ImageDraw.Draw(imagen_final)

        # 4️⃣ Carga de fuentes (con respaldo para evitar 'list index error')
        try:
            font_path = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
            font_nombre = ImageFont.truetype(font_path, 80)
            font_frase = ImageFont.truetype(font_path, 52)
        except:
            font_nombre = font_frase = ImageFont.load_default()

        # 5️⃣ Dibujar textos con seguridad (.get para evitar diccionarios vacíos)
        y_base = alto_p - 480
        nombre_prod = info_producto.get('nombre', 'DarpePro').upper()
        
        draw.text((ancho_p // 2, y_base), nombre_prod, font=font_nombre, fill="white", anchor="mm")
        draw.text((ancho_p // 2, y_base + 95), frase_ia, font=font_frase, fill="#F5F5F5", anchor="mm")

        # 6️⃣ Guardar con puntero reseteado para IMGBB (Evita que se cuelgue)
        buffer = BytesIO()
        imagen_final.save(buffer, format="JPEG", quality=95)
        buffer.seek(0)

        # 7️⃣ Subida a IMGBB
        api_key = st.secrets["IMGBB_API_KEY"]
        files = {"image": ("campaña.jpg", buffer)}
        res_imgbb = requests.post(f"https://api.imgbb.com/1/upload?key={api_key}", files=files)
        
        if res_imgbb.status_code == 200:
            return res_imgbb.json()["data"]["url"]
        else:
            return None

    except Exception as e:
        st.error(f"⚠️ Error en editor_grafico: {e}")
        return None
