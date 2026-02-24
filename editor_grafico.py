import streamlit as st
import base64
import qrcode
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont, ImageChops, ImageOps
import requests

def aplicar_plantilla_y_texto_base64(img_base64, info_producto):
    try:
        # 1. Desencriptar Base64
        img_data = base64.b64decode(img_base64)
        img_ia = Image.open(BytesIO(img_data)).convert("RGB")
        
        # 2. Cargar Plantilla DarpePRO
        try:
            plantilla = Image.open("Plantilla DarpePRO.jpeg").convert("RGB")
        except:
            plantilla = Image.new("RGB", (1080, 1080), (10, 10, 10))

        ancho, alto = plantilla.size
        
        # 3. Mezclar Imagen
        fondo_ia = ImageOps.fit(img_ia, (ancho, alto), Image.LANCZOS)
        imagen_final = ImageChops.multiply(fondo_ia, plantilla)
        
        # 4. QR del producto (Enlace automático)
        qr = qrcode.make(info_producto.get('url', 'https://darpepro.com')).convert('RGB').resize((160, 160))
        imagen_final.paste(qr, (ancho - 200, alto - 200))
        
        # 5. Dibujar NOMBRE DEL PRODUCTO (Sin frases extra)
        draw = ImageDraw.Draw(imagen_final)
        try:
            # Ajusta la ruta a la fuente de tu servidor
            font = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf", 80)
        except:
            font = ImageFont.load_default()

        # Texto centrado en la parte inferior sobre el diseño
        nombre_prod = info_producto['nombre'].upper()
        draw.text((ancho // 2, alto - 320), nombre_prod, font=font, fill="white", anchor="mm")
        
        # 6. Subir resultado a IMGBB
        buf = BytesIO()
        imagen_final.save(buf, format="JPEG", quality=95)
        buf.seek(0)
        
        r = requests.post(
            f"https://api.imgbb.com/1/upload?key={st.secrets['IMGBB_API_KEY']}", 
            files={"image": buf}
        )
        return r.json()["data"]["url"]

    except Exception as e:
        st.error(f"⚠️ Error en editor: {e}")
        return None
