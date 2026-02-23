import streamlit as st
from darpe_scraper import obtener_producto_aleatorio_total
from editor_grafico import aplicar_plantilla_y_texto
from instagram_bot import publicar_en_instagram
from openai import OpenAI

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if st.button("🚀 Generar y Publicar"):
    with st.status("Procesando...", expanded=True):
        prod = obtener_producto_aleatorio_total()
        
        # GPT Genera la frase
        gpt_res = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": f"Escribe una frase publicitaria de máximo 5 palabras para: {prod['nombre']}"}]
        )
        frase_ia = gpt_res.choices[0].message.content.strip('"')

        # DALL-E Genera la imagen
        img_res = client.images.generate(
            model="dall-e-3",
            prompt=f"Professional product photography of {prod['nombre']}, elegant lighting, 8k",
            size="1024x1024"
        )
        url_ia = img_res.data[0].url

        # Edición y Publicación
        url_final = aplicar_plantilla_y_texto(url_ia, prod, frase_ia)
        if url_final:
            pie = f"🔥 ¡Nuevo! {prod['nombre']}\n✨ {frase_ia}\n🔗 {prod['url']}"
            publicar_en_instagram(url_final, pie, st.secrets["FB_ACCESS_TOKEN"], st.secrets["INSTAGRAM_ID"])
            st.success("✅ ¡Publicado con éxito!")
