import streamlit as st
import requests
import qrcode
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont, ImageChops, ImageOps

def aplicar_plantilla_y_texto(url_ia, info_producto):
    try:
        # 1. Descargar imagen desde URL
        res = requests.get(url_ia, timeout=15)
        img_ia = Image.open(BytesIO(res.content)).convert("RGB")
        
        # 2. Cargar Plantilla
        plantilla = Image.open("Plantilla DarpePRO.jpeg").convert("RGB")
        ancho, alto = plantilla.size
        
        # 3. Mezclar Imagen
        fondo_ia = ImageOps.fit(img_ia, (ancho, alto), Image.LANCZOS)
        imagen_final = ImageChops.multiply(fondo_ia, plantilla)
        
        # 4. QR del producto (Enlace real)
        qr = qrcode.make(info_producto.get('url', 'https://darpepro.com')).convert('RGB').resize((160, 160))
        imagen_final.paste(qr, (ancho - 200, alto - 200))
        
        # 5. Dibujar NOMBRE DEL PRODUCTO REAL (Sin frases adicionales)
        draw = ImageDraw.Draw(imagen_final)
        try:
            # Asegúrate de tener la fuente en tu servidor/PC
            font = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf", 85)
        except:
            font = ImageFont.load_default()

        # Texto: Nombre real del producto en mayúsculas
        nombre_texto = info_producto['nombre'].upper()
        draw.text((ancho // 2, alto - 320), nombre_texto, font=font, fill="white", anchor="mm")
        
        # 6. Subir a IMGBB
        buf = BytesIO()
        imagen_final.save(buf, format="JPEG", quality=95)
        buf.seek(0)
        
        api_key = st.secrets["IMGBB_API_KEY"]
        r = requests.post(f"https://api.imgbb.com/1/upload?key={api_key}", files={"image": buf})
        return r.json()["data"]["url"]

    except Exception as e:
        st.error(f"⚠️ Error en editor: {e}")
        return None
