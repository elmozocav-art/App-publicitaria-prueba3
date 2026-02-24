import streamlit as st
import requests
import base64
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont, ImageChops, ImageOps

def aplicar_plantilla_y_texto_base64(img_base64, info_producto, frase_ia):
    try:
        # 1️⃣ Decodificar la imagen de la IA (Base64 como vimos en el video)
        img_data = base64.b64decode(img_base64)
        img_ia = Image.open(BytesIO(img_data)).convert("RGB")
        
        # 2️⃣ Cargar plantilla DarpePro
        plantilla = Image.open("Plantilla DarpePRO.jpeg").convert("RGB")
        ancho, alto = plantilla.size
        
        # 3️⃣ Integrar imagen IA con la plantilla
        fondo_ia = ImageOps.fit(img_ia, (ancho, alto), Image.LANCZOS)
        imagen_final = ImageChops.multiply(fondo_ia, plantilla)
        
        # 4️⃣ Crear Capa de Diseño (Banner inferior)
        overlay = Image.new('RGBA', (ancho, alto), (0, 0, 0, 0))
        draw_overlay = ImageDraw.Draw(overlay)
        
        # Dibujamos un banner negro semi-transparente abajo
        banner_alto = 220
        draw_overlay.rectangle(
            [0, alto - banner_alto, ancho, alto], 
            fill=(0, 0, 0, 160) # Negro con transparencia
        )
        
        # Combinar el banner con la imagen principal
        imagen_final = Image.alpha_composite(imagen_final.convert('RGBA'), overlay).convert('RGB')
        draw = ImageDraw.Draw(imagen_final)

        # 5️⃣ Tipografías
        font_path = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
        try:
            f_nombre = ImageFont.truetype(font_path, 65)
            f_frase = ImageFont.truetype(font_path, 40)
            f_cta = ImageFont.truetype(font_path, 30)
        except:
            f_nombre = f_frase = f_cta = ImageFont.load_default()

        # 6️⃣ Posicionamiento de Textos en el Banner
        # Nombre del Producto (Arriba en el banner)
        nombre = info_producto.get('nombre', 'DARPEPRO SELECTION').upper()
        draw.text((ancho // 2, alto - 170), nombre, font=f_nombre, fill="#FFFFFF", anchor="mm")
        
        # Frase IA (Debajo del nombre)
        draw.text((ancho // 2, alto - 100), frase_ia, font=f_frase, fill="#FFD700", anchor="mm") # Dorado para resaltar
        
        # Enlace/CTA (Pie del banner)
        link_corto = info_producto.get('url', 'www.darpepro.com').replace("https://", "").replace("www.", "")
        draw.text((ancho // 2, alto - 45), f"DISPONIBLE EN: {link_corto}", font=f_cta, fill="#AAAAAA", anchor="mm")

        # 7️⃣ Exportar y Subir
        buffer = BytesIO()
        imagen_final.save(buffer, format="JPEG", quality=95)
        buffer.seek(0)

        api_key = st.secrets["IMGBB_API_KEY"]
        files = {"image": ("publicacion_darpe.jpg", buffer)}
        res_imgbb = requests.post(f"https://api.imgbb.com/1/upload?key={api_key}", files=files)
        
        return res_imgbb.json()["data"]["url"]

    except Exception as e:
        st.error(f"⚠️ Error en el nuevo diseño: {e}")
        return None
