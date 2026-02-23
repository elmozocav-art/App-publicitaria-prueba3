import streamlit as st
import requests
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont, ImageChops, ImageOps
from urllib.parse import urlparse


def aplicar_plantilla_y_texto(url_ia, info_producto, frase_ia):
    try:
        # 1. Descargar imagen generada por IA
        res = requests.get(url_ia)
        img_ia = Image.open(BytesIO(res.content)).convert("RGB")
        
        # 2. Cargar plantilla base
        plantilla = Image.open("Plantilla DarpePRO.jpeg").convert("RGB")
        ancho_p, alto_p = plantilla.size
        
        # 3. Ajustar imagen IA al tamaño de la plantilla
        fondo_ia = ImageOps.fit(img_ia, (ancho_p, alto_p), Image.LANCZOS)
        
        # 4. Fusionar imagen IA con plantilla (modo multiply)
        imagen_final = ImageChops.multiply(fondo_ia, plantilla)
        
        # 5. Añadir textos
        draw = ImageDraw.Draw(imagen_final)
        
        try:
            font_path = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
            font_nombre = ImageFont.truetype(font_path, 65)
            font_frase = ImageFont.truetype(font_path, 40)
            font_link = ImageFont.truetype(font_path, 28)
        except:
            font_nombre = ImageFont.load_default()
            font_frase = ImageFont.load_default()
            font_link = ImageFont.load_default()

        # Nombre del producto
        draw.text(
            (ancho_p // 2, alto_p - 450),
            info_producto['nombre'].upper(),
            font=font_nombre,
            fill="white",
            anchor="mm"
        )
        
        # Frase publicitaria
        draw.text(
            (ancho_p // 2, alto_p - 370),
            frase_ia,
            font=font_frase,
            fill="#EEEEEE",
            anchor="mm"
        )

        # 🔗 Dominio del producto (más limpio visualmente)
        dominio = urlparse(info_producto['url']).netloc
        link_texto = f"Disponible en: {dominio}"

        draw.text(
            (ancho_p // 2, alto_p - 300),
            link_texto,
            font=font_link,
            fill="#DDDDDD",
            anchor="mm"
        )

        # 6. Guardar imagen final en buffer
        buffer = BytesIO()
        imagen_final.save(buffer, format="JPEG", quality=95)
        
        # 7. Subir a IMGBB
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
