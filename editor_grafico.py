import streamlit as st
import requests
import qrcode
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont, ImageChops, ImageOps

def aplicar_plantilla_y_texto(url_ia, info_producto, frase_ia):
    try:
        # 1. Descargar imagen
        res = requests.get(url_ia, timeout=15)
        img_ia = Image.open(BytesIO(res.content)).convert("RGB")
        
        # 2. Plantilla
        plantilla = Image.open("Plantilla DarpePRO.jpeg").convert("RGB")
        ancho, alto = plantilla.size
        
        # 3. Mezcla
        fondo_ia = ImageOps.fit(img_ia, (ancho, alto), Image.LANCZOS)
        imagen_final = ImageChops.multiply(fondo_ia, plantilla)
        
        # 4. QR del Enlace (Esto es lo que pediste para el producto)
        qr = qrcode.QRCode(box_size=4, border=1)
        qr.add_data(info_producto.get('url', 'https://darpepro.com'))
        qr_img = qr.make_image(fill_color="black", back_color="white").convert('RGB').resize((150, 150))
        imagen_final.paste(qr_img, (ancho - 180, alto - 180))
        
        # 5. Textos
        draw = ImageDraw.Draw(imagen_final)
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf", 60)
        except:
            font = ImageFont.load_default()

        draw.text((ancho // 2, alto - 300), info_producto['nombre'].upper(), font=font, fill="white", anchor="mm")
        draw.text((ancho // 2, alto - 230), frase_ia, font=font, fill="#FFD700", anchor="mm")

        # 6. Subir a IMGBB
        buf = BytesIO()
        imagen_final.save(buf, format="JPEG")
        buf.seek(0)
        r = requests.post(f"https://api.imgbb.com/1/upload?key={st.secrets['IMGBB_API_KEY']}", files={"image": buf})
        return r.json()["data"]["url"]

    except Exception as e:
        st.error(f"Error en editor: {e}")
        return None
