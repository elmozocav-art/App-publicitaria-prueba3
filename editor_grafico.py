import streamlit as st
import requests
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

def aplicar_plantilla_y_texto(url_ia, info_producto, frase_ia):
    try:
        # 1. Cargar Plantilla Original
        plantilla = Image.open("Plantilla DarpePRO.jpeg").convert("RGBA")
        ancho_p, alto_p = plantilla.size # Usamos el tamaño real de tu archivo
        
        # 2. Descargar imagen IA
        res = requests.get(url_ia)
        img_ia = Image.open(BytesIO(res.content)).convert("RGBA")
        
        # 3. REDIMENSIÓN PROFESIONAL
        # Escalamos la imagen de la IA para que cubra el ancho de la plantilla
        # pero la mantenemos centrada verticalmente para no tapar tus logos
        nuevo_ancho = ancho_p
        nuevo_alto = ancho_p # Imagen cuadrada
        img_ia = img_ia.resize((nuevo_ancho, nuevo_alto), Image.LANCZOS)
        
        # Posición: Justo en el centro del Reel (formato 9:16)
        pos_y = (alto_p // 2) - (nuevo_alto // 2)
        plantilla.paste(img_ia, (0, pos_y), img_ia)
        
        # 4. DIBUJAR TEXTOS CON MEJOR FUENTE
        draw = ImageDraw.Draw(plantilla)
        
        # Intentamos cargar fuentes estándar de Linux (Streamlit Cloud)
        try:
            fuente_principal = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf", 60)
            fuente_secundaria = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf", 35)
        except:
            fuente_principal = ImageFont.load_default()
            fuente_secundaria = ImageFont.load_default()

        # Nombre del producto: Color blanco, centrado abajo de la foto
        draw.text((ancho_p//2, pos_y + nuevo_alto + 60), info_producto['nombre'].upper(), 
                  font=fuente_principal, fill="white", anchor="mm")
        
        # Frase IA: Un tono gris suave para que no compita
        draw.text((ancho_p//2, pos_y + nuevo_alto + 130), frase_ia, 
                  font=fuente_secundaria, fill="#E0E0E0", anchor="mm")

        # 5. GUARDAR Y SUBIR
        buffer = BytesIO()
        # Guardamos con calidad máxima (95) para evitar que se vea pixelado
        plantilla.convert("RGB").save(buffer, format="JPEG", quality=95)
        
        api_key = st.secrets["IMGBB_API_KEY"]
        files = {"image": ("reel_darpepro.jpg", buffer.getvalue())}
        res_imgbb = requests.post(f"https://api.imgbb.com/1/upload?key={api_key}", files=files)
        
        return res_imgbb.json()["data"]["url"]
        
    except Exception as e:
        st.error(f"Fallo en el diseño: {e}")
        return None
