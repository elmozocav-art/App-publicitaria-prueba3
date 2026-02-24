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

        # 1️⃣ Obtener producto (Con respaldo si falla el scraper)
        prod = obtener_producto_aleatorio_total()
        if not prod:
            st.warning("⚠️ Scraper fallido. Usando producto de reserva.")
            prod = {"nombre": "DarpePro Premium", "url": "https://darpepro.com"}

        # 2️⃣ Texto IA (Blindado contra errores de formato)
        frase_ia = "Domina el momento"
        escenario_ia = "Luxury studio, soft shadows"
        try:
            diseño_ia = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": f"Producto: {prod['nombre']}. Crea FRASE: (5 palabras) | ESCENARIO: (inglés)."}]
            )
            res = diseño_ia.choices[0].message.content
            if "|" in res:
                frase_ia = res.split("|")[0].replace("FRASE:", "").strip()
                escenario_ia = res.split("|")[1].replace("ESCENARIO:", "").strip()
        except:
            st.info("ℹ️ Usando frase de respaldo.")

        # 3️⃣ Imagen (Con corrección de calidad según logs)
        st.write("📸 Generando imagen...")
        url_ia = None
        try:
            img_res = client.images.generate(
                model="gpt-image-1",
                prompt=f"Commercial photo of {prod['nombre']}, {escenario_ia}",
                size="1024x1024",
                quality="high" # 'high' es el valor correcto para este modelo
            )
            if img_res.data:
                url_ia = img_res.data[0].url
        except Exception as e:
            st.error(f"❌ Error en IA de imagen: {e}")

        # 4️⃣ Editor y Publicación
        if url_ia:
            st.write("🛠️ Finalizando diseño...")
            url_final = aplicar_plantilla_y_texto(url_ia, prod, frase_ia)
            
            if url_final:
                publicar_en_instagram(url_final, f"🔥 {prod['nombre']}\n✨ {frase_ia}", st.secrets["FB_ACCESS_TOKEN"], st.secrets["INSTAGRAM_ID"])
                st.success("✅ Campaña en Instagram")
            else:
                st.error("❌ El editor no pudo generar la imagen final.")
        
        status.update(label="Proceso terminado", state="complete")
