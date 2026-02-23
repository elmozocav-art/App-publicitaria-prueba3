import streamlit as st
import requests
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont, ImageChops, ImageOps


def aplicar_plantilla_y_texto(url_ia, info_producto, frase_ia):
    try:
        # 1️⃣ Descargar imagen IA
        res = requests.get(url_ia)
        img_ia = Image.open(BytesIO(res.content)).convert("RGB")
        
        # 2️⃣ Cargar plantilla
        plantilla = Image.open("Plantilla DarpePRO.jpeg").convert("RGB")
        ancho_p, alto_p = plantilla.size
        
        # 3️⃣ Ajustar imagen IA
        fondo_ia = ImageOps.fit(img_ia, (ancho_p, alto_p), Image.LANCZOS)
        imagen_final = ImageChops.multiply(fondo_ia, plantilla)
        
        draw = ImageDraw.Draw(imagen_final)

        # 4️⃣ Fuentes más grandes y mejor proporción
        try:
            font_path = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
            font_nombre = ImageFont.truetype(font_path, 80)
            font_frase = ImageFont.truetype(font_path, 55)
            font_link = ImageFont.truetype(font_path, 32)
        except:
            font_nombre = ImageFont.load_default()
            font_frase = ImageFont.load_default()
            font_link = ImageFont.load_default()

        # 5️⃣ POSICIONES MÁS COMPACTAS
        y_base = alto_p - 500

        # Nombre producto
        draw.text(
            (ancho_p // 2, y_base),
            info_producto['nombre'].upper(),
            font=font_nombre,
            fill="white",
            anchor="mm"
        )

        # Frase más grande y más cerca
        draw.text(
            (ancho_p // 2, y_base + 90),
            frase_ia,
            font=font_frase,
            fill="#F0F0F0",
            anchor="mm"
        )

        # 🔗 ENLACE COMPLETO DEL PRODUCTO ESPECÍFICO
        link_texto = f"Compra ahora: {info_producto['url']}"

        draw.text(
            (ancho_p // 2, y_base + 170),
            link_texto,
            font=font_link,
            fill="#DDDDDD",
            anchor="mm"
        )

        # 6️⃣ Guardar imagen final
        buffer = BytesIO()
        imagen_final.save(buffer, format="JPEG", quality=95)

        # 7️⃣ Subir a IMGBB
        api_key = st.secrets["IMGBB_API_KEY"]
        files = {"image": ("reel_final.jpg", buffer.getvalue())}
        res_imgbb = requests.post(
            f"https://api.imgbb.com/1/upload?key={api_key}",
            files=files
        )

        return res_imgbb.json()["data"]["url"]

    except Exception as e:
        st.error(f"Fallo en el editor: {e}")
        return None
