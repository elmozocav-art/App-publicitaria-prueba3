import streamlit as st
import requests
import qrcode
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont, ImageChops, ImageOps

def aplicar_plantilla_y_texto(url_ia, info_producto, frase_ia):
    # BLINDAJE: Si no hay URL, salimos para evitar el error 'NoneType'
    if not url_ia:
        return None
    
    try:
        # 1️⃣ Descargar imagen desde la URL de OpenAI
        res = requests.get(url_ia, timeout=15)
        img_ia = Image.open(BytesIO(res.content)).convert("RGB")
        
        # 2️⃣ Cargar plantilla DarpePro
        try:
            plantilla = Image.open("Plantilla DarpePRO.jpeg").convert("RGB")
        except:
            st.error("❌ No se encontró la plantilla física. Usando fondo oscuro.")
            plantilla = Image.new("RGB", (1080, 1080), (15, 15, 15))

        ancho, alto = plantilla.size
        
        # 3️⃣ Integrar imagen con plantilla
        fondo_ia = ImageOps.fit(img_ia, (ancho, alto), Image.LANCZOS)
        imagen_final = ImageChops.multiply(fondo_ia, plantilla)
        
        # 4️⃣ Generar Código QR con el enlace al producto
        qr = qrcode.QRCode(box_size=4, border=1)
        qr.add_data(info_producto.get('url', 'https://darpepro.com'))
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="black", back_color="white").convert('RGB')
        qr_img = qr_img.resize((150, 150))
        
        # Pegar QR en la esquina
        imagen_final.paste(qr_img, (ancho - 180, alto - 180))
        
        draw = ImageDraw.Draw(imagen_final)

        # 5️⃣ Tipografías con respaldo
        font_path = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
        try:
            f_nombre = ImageFont.truetype(font_path, 75)
            f_frase = ImageFont.truetype(font_path, 45)
            f_cta = ImageFont.truetype(font_path, 25)
        except:
            f_nombre = f_frase = f_cta = ImageFont.load_default()

        # 6️⃣ Textos finales
        nombre = info_producto.get('nombre', 'DARPEPRO').upper()
        draw.text((ancho // 2, alto - 350), nombre, font=f_nombre, fill="white", anchor="mm")
        draw.text((ancho // 2, alto - 280), frase_ia, font=f_frase, fill="#FFD700", anchor="mm")
        draw.text((ancho - 105, alto - 25), "ESCANEA Y COMPRA", font=f_cta, fill="white", anchor="mm")

        # 7️⃣ Guardar y Subir a IMGBB
        buffer = BytesIO()
        imagen_final.save(buffer, format="JPEG", quality=95)
        buffer.seek(0)

        api_key = st.secrets["IMGBB_API_KEY"]
        files = {"image": ("campana_darpe.jpg", buffer)}
        res_imgbb = requests.post(f"https://api.imgbb.com/1/upload?key={api_key}", files=files)
        
        return res_imgbb.json()["data"]["url"]

    except Exception as e:
        st.error(f"⚠️ Error en editor: {e}")
        return None
