import streamlit as st
import base64
import qrcode
import requests
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont, ImageChops, ImageOps

def aplicar_plantilla_y_texto_base64(img_codificada, info_producto):
    try:
        # 1. Decodificar la imagen Base64 de la IA
        img_data = base64.b64decode(img_codificada)
        img_ia = Image.open(BytesIO(img_data)).convert("RGB")
        
        # 2. Cargar tu Plantilla DarpePRO
        plantilla = Image.open("Plantilla DarpePRO.jpeg").convert("RGB")
        ancho, alto = plantilla.size
        
        # 3. Integración de la imagen en la plantilla
        fondo_ia = ImageOps.fit(img_ia, (ancho, alto), Image.LANCZOS)
        imagen_final = ImageChops.multiply(fondo_ia, plantilla)
        
        # 4. Generar QR automático con la URL del producto
        qr = qrcode.make(info_producto.get('url', 'https://darpepro.com')).convert('RGB').resize((165, 165))
        imagen_final.paste(qr, (ancho - 205, alto - 205))
        
        # 5. Escribir el NOMBRE REAL (Pisa cualquier texto que la IA haya intentado poner)
        draw = ImageDraw.Draw(imagen_final)
        try:
            # Fuente gruesa para que resalte
            font = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf", 85)
        except:
            font = ImageFont.load_default()

        nombre_texto = info_producto['nombre'].upper()
        # Texto blanco con borde negro para máxima legibilidad
        draw.text((ancho // 2, alto - 320), nombre_texto, font=font, fill="white", 
                  anchor="mm", stroke_width=3, stroke_fill="black")
        
        # 6. Subir resultado a IMGBB para Instagram
        buf = BytesIO()
        imagen_final.save(buf, format="JPEG", quality=95)
        buf.seek(0)
        r = requests.post(f"https://api.imgbb.com/1/upload?key={st.secrets['IMGBB_API_KEY']}", files={"image": buf})
        return r.json()["data"]["url"]

    except Exception as e:
        st.error(f"⚠️ Error en el proceso de imagen: {e}")
        return None
