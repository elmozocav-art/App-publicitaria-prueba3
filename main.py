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

        # 1. Producto
        prod = obtener_producto_aleatorio_total() or {"nombre": "DarpePro Premium", "url": "https://darpepro.com"}

        # 2. IA de Texto
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
            st.warning("⚠️ Aviso en GPT: Usando valores por defecto.")

        # 3. Generar Imagen (CORRECCIÓN: Sin parámetros que den Error 400)
        st.write("📸 Generando imagen profesional...")
        url_ia = None
        try:
            # Quitamos 'response_format' y 'background' para evitar el Error 400
            img_res = client.images.generate(
                model="gpt-image-1",
                prompt=f"Professional photo of {prod['nombre']}, {escenario_ia}",
                size="1024x1024",
                quality="high" # Calidad aceptada según tus logs
            )
            
            # Verificamos la URL para evitar el error 'NoneType'
            if img_res.data and img_res.data[0].url:
                url_ia = img_res.data[0].url
                st.write("✅ Imagen generada correctamente.")
            else:
                st.error("⚠️ OpenAI no devolvió una URL válida.")
        except Exception as e:
            st.error(f"❌ Error en la API: {e}")

        # 4. Procesar y Publicar
        if url_ia:
            st.write("🛠️ Aplicando marca y QR...")
            url_final = aplicar_plantilla_y_texto(url_ia, prod, frase_ia)
            
            if url_final:
                caption = f"✨ {frase_ia}\n\n🛍️ {prod['nombre'].upper()}\n🛒 {prod['url']}\n👉 Escanea el QR para comprar!"
                publicar_en_instagram(url_final, caption, st.secrets["FB_ACCESS_TOKEN"], st.secrets["INSTAGRAM_ID"])
                st.success("✅ ¡Campaña publicada!")
        
        status.update(label="Proceso terminado", state="complete")
