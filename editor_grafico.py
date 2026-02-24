import streamlit as st
import requests
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont, ImageChops, ImageOps

def aplicar_plantilla_y_texto(url_ia, info_producto, frase_ia):
    if not url_ia:
        st.error("Error: No se recibió una URL de imagen válida.")
        return None
        
    try:
        # 1️⃣ Descargar imagen IA con validación de estado
        res = requests.get(url_ia, timeout=15)
        if res.status_code != 200:
            raise Exception(f"No se pudo descargar la imagen de la IA. Status: {res.status_code}")
            
        img_ia = Image.open(BytesIO(res.content)).convert("RGB")
        
        # 2️⃣ Cargar plantilla (con verificación de existencia)
        try:
            plantilla = Image.open("Plantilla DarpePRO.jpeg").convert("RGB")
        except FileNotFoundError:
            st.warning("⚠️ No se encontró 'Plantilla DarpePRO.jpeg'. Usando fondo limpio.")
            plantilla = Image.new("RGB", (1080, 1080), (20, 20, 20))
            
        ancho_p, alto_p = plantilla.size
        
        # 3️⃣ Mezcla de alta calidad (Multiplicación de capas)
        fondo_ia = ImageOps.fit(img_ia, (ancho_p, alto_p), Image.LANCZOS)
        imagen_final = ImageChops.multiply(fondo_ia, plantilla)
        
        draw = ImageDraw.Draw(imagen_final)

        # 4️⃣ Gestión inteligente de fuentes
        try:
            # Ruta común en servidores Linux (Streamlit Cloud)
            font_path = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
            font_nombre = ImageFont.truetype(font_path, 85)
            font_frase = ImageFont.truetype(font_path, 58)
            font_link = ImageFont.truetype(font_path, 34)
        except:
            # Respaldo si no hay fuentes instaladas
            st.info("ℹ️ Fuentes del sistema no detectadas, usando tipografía básica.")
            font_nombre = font_frase = font_link = ImageFont.load_default()

        # 5️⃣ Posicionamiento dinámico (Basado en el alto de la imagen)
        y_base = alto_p - 450 

        # Texto: Nombre Producto (Sombra para legibilidad)
        texto_nombre = info_producto.get('nombre', 'Producto DarpePro').upper()
        draw.text((ancho_p // 2 + 2, y_base + 2), texto_nombre, font=font_nombre, fill="black", anchor="mm")
        draw.text((ancho_p // 2, y_base), texto_nombre, font=font_nombre, fill="white", anchor="mm")

        # Texto: Frase de Marketing
        draw.text((ancho_p // 2, y_base + 100), frase_ia, font=font_frase, fill="#E0E0E0", anchor="mm")

        # Texto: Link de Compra
        link_texto = f"Link en Bio: {info_producto.get('url', 'darpepro.com')}"
        draw.text((ancho_p // 2, y_base + 190), link_texto, font=font_link, fill="#BBBBBB", anchor="mm")

        # 6️⃣ Guardar y exportar con alta calidad
        buffer = BytesIO()
        imagen_final.save(buffer, format="JPEG", quality=95, subsampling=0)
        buffer.seek(0) # Resetear puntero del buffer para la subida

        # 7️⃣ Subir a IMGBB
        api_key = st.secrets["IMGBB_API_KEY"]
        files = {"image": ("campaña_darpe.jpg", buffer)}
        res_imgbb = requests.post(
            f"https://api.imgbb.com/1/upload?key={api_key}",
            files=files
        )
        
        if res_imgbb.status_code == 200:
            return res_imgbb.json()["data"]["url"]
        else:
            st.error(f"Error en IMGBB: {res_imgbb.text}")
            return None

    except Exception as e:
        st.error(f"⚠️ Error crítico en editor_grafico: {str(e)}")
        return None
