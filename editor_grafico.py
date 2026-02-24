import streamlit as st
import requests
import base64 # <--- NECESARIO PARA DESENCRIPTAR
import qrcode
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont, ImageChops, ImageOps

def aplicar_plantilla_y_texto_base64(datos_b64, info_producto, frase_ia):
    try:
        # 1️⃣ DESENCRIPTAR: Convertir Base64 a Imagen
        img_data = base64.b64decode(datos_b64)
        img_ia = Image.open(BytesIO(img_data)).convert("RGB")
        
        # 2️⃣ Cargar plantilla
        try:
            plantilla = Image.open("Plantilla DarpePRO.jpeg").convert("RGB")
        except:
            plantilla = Image.new("RGB", (1080, 1080), (15, 15, 15))

        ancho, alto = plantilla.size
        
        # 3️⃣ Integración
        fondo_ia = ImageOps.fit(img_ia, (ancho, alto), Image.LANCZOS)
        imagen_final = ImageChops.multiply(fondo_ia, plantilla)
        
        # 4️⃣ Generar QR con el enlace
        qr = qrcode.QRCode(box_size=4, border=1)
        qr.add_data(info_producto.get('url', 'https://darpepro.com'))
        qr_img = qr.make_image(fill_color="black", back_color="white").convert('RGB').resize((150, 150))
        imagen_final.paste(qr_img, (ancho - 180, alto - 180))
        
        # 5️⃣ Textos
        draw = ImageDraw.Draw(imagen_final)
        font_path = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
        try:
            f_nombre = ImageFont.truetype(font_path, 75)
            f_frase = ImageFont.truetype(font_path, 45)
        except:
            f_nombre = f_frase = ImageFont.load_default()

        nombre = info_producto.get('nombre', 'DARPEPRO').upper()
        draw.text((ancho // 2, alto - 350), nombre, font=f_nombre, fill="white", anchor="mm")
        draw.text((ancho // 2, alto - 280), frase_ia, font=f_frase, fill="#FFD700", anchor="mm")

        # 6️⃣ Guardar y Subir
        buffer = BytesIO()
        imagen_final.save(buffer, format="JPEG", quality=95)
        buffer.seek(0)

        api_key = st.secrets["IMGBB_API_KEY"]
        files = {"image": ("post.jpg", buffer)}
        res_imgbb = requests.post(f"https://api.imgbb.com/1/upload?key={api_key}", files=files)
        
        return res_imgbb.json()["data"]["url"]

    except Exception as e:
        st.error(f"⚠️ Error desencriptando imagen: {e}")
        return None
