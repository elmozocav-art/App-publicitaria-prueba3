import streamlit as st
from darpe_scraper import obtener_producto_aleatorio_total
from editor_grafico import aplicar_plantilla_y_texto
from instagram_bot import publicar_en_instagram
from openai import OpenAI

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if st.button("🚀 Lanzar Campaña de Categorías"):
    with st.status("📁 Explorando las 12 categorías...", expanded=True) as status:
        prod = obtener_producto_aleatorio_total()
        
        if not prod:
            st.error("❌ Error Crítico: No se pudo conectar con las categorías.")
            st.stop()

        st.success(f"📦 Producto encontrado: **{prod['nombre']}**")

        # GPT crea el escenario pero DALL-E tiene prohibido escribir
        diseño = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": "NUNCA incluyas texto o etiquetas en la imagen."},
                      {"role": "user", "content": f"Escenario de lujo para {prod['nombre']}. FRASE: [5 palabras] | ESCENARIO: [ingles]"}]
        )
        resp = diseño.choices[0].message.content
        frase_ia = resp.split("|")[0].replace("FRASE:", "").strip()
        escenario_ia = resp.split("|")[1].replace("ESCENARIO:", "").strip()

        # Generar imagen limpia (Sin la palabra 'PRODUCTO')
        img_res = client.images.generate(
            model="dall-e-3",
            prompt=f"Professional product photography of {prod['nombre']} in {escenario_ia}. NO TEXT, NO LABELS.",
            size="1024x1024"
        )
        url_ia = img_res.data[0].url

        # Fusión de plantilla y escritura del NOMBRE REAL por Python
        url_final = aplicar_plantilla_y_texto(url_ia, prod, frase_ia)

        if url_final:
            pie = f"🔥 {prod['nombre']} \n✨ {frase_ia} \n\n🔗 Compra aquí: {prod['url']}"
            publicar_en_instagram(url_final, pie, st.secrets["FB_ACCESS_TOKEN"], st.secrets["INSTAGRAM_ID"])
            st.success(f"✅ ¡Publicado! Enlace: {prod['url']}")
