import streamlit as st
from darpe_scraper import obtener_producto_aleatorio_total
from editor_grafico import aplicar_plantilla_y_texto
from instagram_bot import publicar_en_instagram
from openai import OpenAI

st.set_page_config(page_title="DarpePro AI-Director", layout="centered")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("🎬 Director Creativo DarpePro")

if st.button("🚀 Generar Campaña Inteligente"):

    with st.status("🤖 IA trabajando...", expanded=True) as status:

        # 1️⃣ Obtener producto
        prod = obtener_producto_aleatorio_total()

        st.write(f"📦 Producto detectado: **{prod['nombre']}**")
        st.write(f"🔗 Enlace detectado: {prod['url']}")

        # 2️⃣ MEJORA EN TEXTO: Instrucciones de Neuromarketing
        diseño_ia = client.chat.completions.create(
            model="gpt-4o", # He subido a 4o para frases mucho más humanas y vendedoras
            messages=[
                {
                    "role": "system", 
                    "content": "Eres un Director Creativo de marcas de lujo como Apple o Nike. Creas deseo de compra."
                },
                {
                    "role": "user", 
                    "content": f"""
Para el producto '{prod['nombre']}':

1. Crea una frase de marketing emocional y potente (máximo 5 palabras). No uses palabras trilladas como 'increíble'.
2. Describe un escenario fotográfico minimalista y caro en inglés (cinematic, soft shadows, premium textures).

Formato:
FRASE: texto | ESCENARIO: texto
"""
                }
            ]
        )

        respuesta = diseño_ia.choices[0].message.content

        try:
            frase_ia = respuesta.split("|")[0].replace("FRASE:", "").strip()
            escenario_ia = respuesta.split("|")[1].replace("ESCENARIO:", "").strip()
        except:
            frase_ia = "La perfección en tus manos"
            escenario_ia = "Minimalist luxury studio, soft directional lighting, elegant shadows"

        st.write(f"✨ Frase: {frase_ia}")

        # 3️⃣ MEJORA EN IMAGEN: Prompt de Fotografía Realista
        # Hemos añadido detalles de lente, iluminación y texturas para evitar el "look IA"
        prompt_final = (
            f"High-end commercial studio photography of {prod['nombre']}. "
            f"Concept: {escenario_ia}. "
            f"Shot on 85mm lens, f/4.0 aperture, natural soft shadows, hyper-realistic, "
            f"8k resolution, professional color grading, clean composition, NO text."
        )

        img_res = client.images.generate(
            model="dall-e-3",
            prompt=prompt_final,
            size="1024x1024",
            quality="hd" # Manteniendo HD para máxima nitidez
        )

        url_ia = img_res.data[0].url
        st.image(url_ia)

        # 4️⃣ Aplicar plantilla
        url_final = aplicar_plantilla_y_texto(url_ia, prod, frase_ia)

        if not url_final:
            st.error("Error generando imagen final.")
            st.stop()

        # 5️⃣ MEJORA EN CAPTION: Emojis y estructura limpia
        caption = (
            f"🔥 {prod['nombre'].upper()}\n\n"
            f"✨ {frase_ia}\n\n"
            f"Un nuevo nivel de diseño y funcionalidad llega a DarpePro. 🚀\n\n"
            f"🛒 Adquiérelo aquí:\n"
            f"{prod['url']}\n\n"
            f"#DarpePro #Exclusivo #TechStyle #Design"
        )

        # 6️⃣ Publicar
        resultado = publicar_en_instagram(
            url_final,
            caption,
            st.secrets["FB_ACCESS_TOKEN"],
            st.secrets["INSTAGRAM_ID"]
        )

        if isinstance(resultado, dict) and "id" in resultado:
            st.success("✅ ¡Publicado correctamente!")
        else:
            st.error(f"Error al publicar: {resultado}")

        status.update(label="✅ Proceso completado", state="complete")
