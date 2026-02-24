import streamlit as st
from darpe_scraper import obtener_producto_aleatorio_total
from editor_grafico import procesar_imagen_auto
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
        try:
            res_txt = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": f"Producto: {prod['nombre']}. FRASE: (5 palabras) | ESCENARIO: (inglés)."}]
            ).choices[0].message.content
            if "|" in res_txt:
                frase_ia = res_txt.split("|")[0].replace("FRASE:", "").strip()
        except:
            st.warning("⚠️ Usando textos por defecto.")

        # 3. Generar Imagen (Detección automática de formato)
        st.write("📸 Generando imagen profesional...")
        img_data_ia = None
        try:
            # NO usamos 'response_format' ni 'background' para evitar el Error 400
            img_res = client.images.generate(
                model="gpt-image-1",
                prompt=f"Professional luxury photo of {prod['nombre']}",
                size="1024x1024",
                quality="high"
            )
            
            # Verificamos qué nos envió la API para evitar el error 'NoneType'
            if img_res.data:
                # Si envió URL, la usamos. Si envió Base64 (b64_json), también.
                img_data_ia = getattr(img_res.data[0], 'url', None) or getattr(img_res.data[0], 'b64_json', None)
            
            if not img_data_ia:
                st.error("⚠️ La IA no devolvió datos válidos (URL/Base64).")
        except Exception as e:
            st.error(f"❌ Error en la API: {e}")

        # 4. Procesar con el nuevo Editor Auto
        if img_data_ia:
            st.write("🛠️ Aplicando marca y QR...")
            url_final = procesar_imagen_auto(img_data_ia, prod, frase_ia)
            
            if url_final:
                caption = f"✨ {frase_ia}\n\n🛍️ {prod['nombre'].upper()}\n🛒 {prod['url']}\n👉 Escanea el QR para comprar!"
                publicar_en_instagram(url_final, caption, st.secrets["FB_ACCESS_TOKEN"], st.secrets["INSTAGRAM_ID"])
                st.success("✅ ¡Campaña publicada!")
        
        status.update(label="Proceso terminado", state="complete")
