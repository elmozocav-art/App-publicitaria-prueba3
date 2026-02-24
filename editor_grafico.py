import streamlit as st
import base64
import qrcode
import requests
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont, ImageChops, ImageOps

def aplicar_plantilla_y_texto_base64(img_codificada, info_producto):
    try:
        # 1. Decodificar Base64
        img_data = base64.b64decode(img_codificada)
        img_ia = Image.open(BytesIO(img_data)).convert("RGB")
        
        # 2. Cargar Plantilla
        plantilla = Image.open("Plantilla DarpePRO.jpeg").convert("RGB")
        ancho, alto = plantilla.size
        
        # 3. Mezcla de Imagen
        fondo_ia = ImageOps.fit(img_ia, (ancho, alto), Image.LANCZOS)
        imagen_final = ImageChops.multiply(fondo_ia, plantilla)
        
        # 4. QR con enlace real (Visto en tu resultado)
        qr = qrcode.make(info_producto.get('url', 'https://darpepro.com')).convert('RGB').resize((160, 160))
        imagen_final.paste(qr, (ancho - 200, alto - 200))
        
        # 5. Escribir NOMBRE REAL DEL PRODUCTO (Limpiando la imagen)
        draw = ImageDraw.Draw(imagen_final)
        try:
            # Ajusta esta ruta a la fuente que tengas instalada
            font = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf", 85)
        except:
            font = ImageFont.load_default()

        # Ponemos el nombre del producto en mayúsculas, centrado
        nombre_real = info_producto['nombre'].upper()
        draw.text((ancho // 2, alto - 320), nombre_real, font=font, fill="white", anchor="mm")
        
        # 6. Subir a IMGBB
        buf = BytesIO()
        imagen_final.save(buf, format="JPEG", quality=95)
        buf.seek(0)
        r = requests.post(f"https://api.imgbb.com/1/upload?key={st.secrets['IMGBB_API_KEY']}", files={"image": buf})
        return r.json()["data"]["url"]

    except Exception as e:
        st.error(f"⚠️ Error en editor: {e}")
        return None
