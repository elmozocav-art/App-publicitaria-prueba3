import streamlit as st
import base64
from darpe_scraper import obtener_producto_aleatorio_total
from editor_grafico import aplicar_plantilla_y_texto_base64
from instagram_bot import publicar_en_instagram
from openai import OpenAI

st.set_page_config(page_title="DarpePro AI-Director", layout="centered")
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("🎬 Director Creativo DarpePro")

if st.button("🚀 Generar Campaña Inteligente"):
    with st.status("🤖 IA trabajando...", expanded=True) as status:

        # 1️⃣ Obtener producto
        prod = obtener_producto_aleatorio_total()
        if not prod:
            prod = {"nombre": "DarpePro Premium", "url": "https://darpepro.com"}

        # 2️⃣ Texto IA
        frase_ia = "Innovación en cada detalle"
        escenario_ia = "Modern luxury studio, cinematic lighting"
        try:
            diseño_ia = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": f"Producto: {prod['nombre']}. FRASE: (5 palabras) | ESCENARIO: (inglés)."}]
            )
            res = diseño_ia.choices[0].message.content
            if "|" in res:
                frase_ia = res.split("|")[0].replace("FRASE:", "").strip()
                escenario_ia = res.split("|")[1].replace("ESCENARIO:", "").strip()
        except:
            st.warning("⚠️ Usando valores por defecto.")

        # 3️⃣ Generar Imagen (Siguiendo parámetros del video)
        st.write("📸 Generando imagen (Base64)...")
        img_base64 = None
        try:
            img_res = client.images.generate(
                model="gpt-image-1",
                prompt=f"Professional photo of {prod['nombre']}, {escenario_ia}",
                size="1024x1024",
                quality="high",        # <-- 'high' según el video
                background="opaque"    # <-- Parámetro exclusivo de gpt-image-1
            )
            # El video explica que gpt-image-1 devuelve la imagen en el campo 'b64_json' o similar
            if img_res and img_res.data:
                img_base64 = img_res.data[0].b64_json  # Accedemos al contenido Base64
        except Exception as e:
            st.error(f"❌ Error en el modelo: {e}")

        # 4️⃣ Enviar al editor especial
        if img_base64:
            st.write("🛠️ Procesando diseño...")
            url_final = aplicar_plantilla_y_texto_base64(img_base64, prod, frase_ia)
            
            if url_final:
                publicar_en_instagram(url_final, f"✨ {frase_ia}", st.secrets["FB_ACCESS_TOKEN"], st.secrets["INSTAGRAM_ID"])
                st.success("✅ Campaña publicada")
        
        status.update(label="Completado", state="complete")
