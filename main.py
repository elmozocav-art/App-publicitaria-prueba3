import streamlit as st
from darpe_scraper import obtener_producto_aleatorio_total
from editor_grafico import aplicar_plantilla_y_texto
from instagram_bot import publicar_en_instagram
from openai import OpenAI

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if st.button("🚀 Publicar en Instagram (12 Categorías)"):
    with st.status("🤖 Conectando con DarpePro...", expanded=True):
        prod = obtener_producto_aleatorio_total()
        
        if not prod:
            st.error("❌ Fallo de conexión. La web no responde.")
            st.stop()

        st.info(f"🔗 Enlace directo: {prod['url']}")

        # GPT crea el escenario (Prohibimos texto)
        diseño = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": "Director de arte. NUNCA escribas texto en la imagen."},
                      {"role": "user", "content": f"Escenario premium para {prod['nombre']}. FRASE: [5 palabras] | ESCENARIO: [ingles]"}]
        )
        resp = diseño.choices[0].message.content
        frase_ia = resp.split("|")[0].replace("FRASE:", "").strip()
        escenario_ia = resp.split("|")[1].replace("ESCENARIO:", "").strip()

        # DALL-E: Foto limpia (Sin el error de 'PRODUCTO')
        prompt_final = f"Professional product photo of {prod['nombre']} in {escenario_ia}. NO TEXT, NO LABELS."
        img_res = client.images.generate(model="dall-e-3", prompt=prompt_final)
        url_ia = img_res.data[0].url

        # Editor: Pone tu plantilla y el nombre REAL con Python
        url_final = aplicar_plantilla_y_texto(url_ia, prod, frase_ia)

        if url_final:
            pie = f"🔥 {prod['nombre']} \n✨ {frase_ia} \n\n🔗 Compra aquí: {prod['url']}"
            publicar_en_instagram(url_final, pie, st.secrets["FB_ACCESS_TOKEN"], st.secrets["INSTAGRAM_ID"])
            st.success("✅ ¡Publicado con éxito!")
