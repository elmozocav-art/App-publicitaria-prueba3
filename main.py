import streamlit as st
import requests
import json
from darpe_scraper import obtener_producto_aleatorio_total
from editor_grafico import aplicar_plantilla_y_texto
from instagram_bot import publicar_en_instagram
from openai import OpenAI

st.set_page_config(page_title="DarpePro AI-Director", layout="centered")

# Configuración de API
API_KEY = st.secrets["OPENAI_API_KEY"]
client = OpenAI(api_key=API_KEY)

st.title("🎬 Director Creativo DarpePro")

if st.button("🚀 Generar Campaña Inteligente"):

    with st.status("🤖 IA trabajando...", expanded=True) as status:

        # 1️⃣ Obtener producto
        prod = obtener_producto_aleatorio_total()
        if not prod:
            st.error("No se pudo obtener producto de la web.")
            st.stop()

        st.write(f"📦 Producto: **{prod['nombre']}**")

        # 2️⃣ Generar Prompt Maestro (GPT-4o)
        # Usamos un modelo superior para describir la escena como un fotógrafo real
        diseño_ia = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Eres un Director Creativo de lujo. Generas descripciones técnicas de fotografía."},
                {"role": "user", "content": f"Producto: {prod['nombre']}. Crea: 1. Frase de venta (5 palabras). 2. Descripción visual detallada en inglés para IA de imagen (estilo premium, 85mm, cinematic lighting). Formato: FRASE: texto | ESCENARIO: texto"}
            ]
        )
        
        respuesta = diseño_ia.choices[0].message.content
        try:
            frase_ia = respuesta.split("|")[0].replace("FRASE:", "").strip()
            escenario_ia = respuesta.split("|")[1].replace("ESCENARIO:", "").strip()
        except:
            frase_ia = "Excelencia en cada detalle"
            escenario_ia = "High-end commercial photography, minimalist studio"

        # 3️⃣ Generar Imagen con GPT Image 1 (Llamada según tutorial)
        st.write("📸 Generando imagen con GPT Image 1...")
        
        prompt_final = (
            f"Official commercial product photography of {prod['nombre']}. "
            f"Scene: {escenario_ia}. Ultra-realistic textures, professional color grading, "
            f"soft shadows, 8k resolution, clean background. No watermarks."
        )

        try:
            # Llamada al modelo específico mencionado en el video
            img_res = client.images.generate(
                model="gpt-image-1", # Cambiado según el nuevo modelo disponible
                prompt=prompt_final,
                size="1024x1024",
                quality="hd" 
            )
            
            if img_res and img_res.data:
                url_ia = img_res.data[0].url
                st.image(url_ia, caption="Resultado GPT Image 1")
            else:
                st.error("El modelo gpt-image-1 no devolvió datos. Revisa la verificación de tu cuenta.")
                st.stop()
        except Exception as e:
            st.error(f"Error en el modelo de imagen: {e}")
            st.stop()

        # 4️⃣ Procesamiento y Publicación
        st.write("🛠️ Finalizando diseño...")
        url_final = aplicar_plantilla_y_texto(url_ia, prod, frase_ia)

        if url_final:
            caption = (
                f"🔥 {prod['nombre'].upper()}\n\n"
                f"✨ {frase_ia}\n\n"
                f"Consigue el tuyo en el enlace de la bio. 🚀\n"
                f"🛒 {prod['url']}\n\n"
                f"#DarpePro #IA #TechLuxury"
            )

            resultado = publicar_en_instagram(
                url_final,
                caption,
                st.secrets["FB_ACCESS_TOKEN"],
                st.secrets["INSTAGRAM_ID"]
            )

            if isinstance(resultado, dict) and "id" in resultado:
                st.success("✅ ¡Publicado en Instagram!")
            else:
                st.error("Fallo en la publicación final.")

        status.update(label="✅ Campaña Completada", state="complete")
