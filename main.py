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

        # 1️⃣ Obtener producto (Con respaldo para evitar error de scraper)
        prod = obtener_producto_aleatorio_total()
        if not prod:
            st.warning("⚠️ Scraper fallido. Usando producto genérico.")
            prod = {"nombre": "DarpePro Premium", "url": "https://darpepro.com"}

        # 2️⃣ Texto IA (Blindado contra errores de formato '|')
        frase_ia = "Calidad que inspira"
        escenario_ia = "Luxury product photography, clean studio background"
        try:
            diseño_ia = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": f"Producto: {prod['nombre']}. Crea FRASE: (5 palabras) | ESCENARIO: (escena en inglés para IA)."}]
            )
            res = diseño_ia.choices[0].message.content
            if "|" in res:
                frase_ia = res.split("|")[0].replace("FRASE:", "").strip()
                escenario_ia = res.split("|")[1].replace("ESCENARIO:", "").strip()
        except:
            st.info("ℹ️ Usando textos de respaldo por fallo en GPT.")

        # 3️⃣ Generar Imagen (CORRECCIÓN DE ERROR 400: quality="high")
        st.write("📸 Generando imagen profesional...")
        url_ia = None
        try:
            img_res = client.images.generate(
                model="gpt-image-1",
                prompt=f"Professional commercial photo of {prod['nombre']}, {escenario_ia}, 8k, sharp focus.",
                size="1024x1024",
                quality="high" # 'high' es el valor correcto, 'hd' causa error 400
            )
            if img_res and img_res.data:
                url_ia = img_res.data[0].url
                st.image(url_ia, caption="Imagen de IA generada")
            else:
                st.error("⚠️ La IA no devolvió datos de imagen.")
        except Exception as e:
            st.error(f"❌ Error crítico en imagen: {e}")

        # 4️⃣ Editor Gráfico y Publicación (Solo si url_ia existe para evitar 'NoneType')
        if url_ia:
            st.write("🛠️ Finalizando diseño con marca DarpePro...")
            url_final = aplicar_plantilla_y_texto(url_ia, prod, frase_ia)
            
            if url_final:
                publicar_en_instagram(
                    url_final, 
                    f"🔥 {prod['nombre'].upper()}\n✨ {frase_ia}\n🛒 {prod['url']}", 
                    st.secrets["FB_ACCESS_TOKEN"], 
                    st.secrets["INSTAGRAM_ID"]
                )
                st.success("✅ Campaña publicada en Instagram")
            else:
                st.error("❌ El editor gráfico falló al procesar la imagen.")
        
        status.update(label="Proceso completado", state="complete")
