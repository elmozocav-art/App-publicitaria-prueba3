import streamlit as st
from darpe_scraper import obtener_producto_aleatorio_total
from editor_grafico import aplicar_plantilla_y_texto_base64
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

        # 3. Generar Imagen (Base64 puro, sin parámetros extra)
        st.write("📸 Generando imagen (Base64)...")
        img_base64 = None
        try:
            # Quitamos 'background' para evitar el Error 400
            img_res = client.images.generate(
                model="gpt-image-1",
                prompt=f"Professional photo of {prod['nombre']}, {escenario_ia}",
                size="1024x1024",
                quality="high",
                response_format="b64_json" # Forzamos el formato que usaba el código anterior
            )
            
            # Verificamos la existencia de datos para evitar 'NoneType'
            if img_res.data and img_res.data[0].b64_json:
                img_base64 = img_res.data[0].b64_json
                st.write("✅ Datos recibidos correctamente.")
            else:
                st.error("⚠️ OpenAI no devolvió datos Base64.")
        except Exception as e:
            st.error(f"❌ Error en la API: {e}")

        # 4. Procesar y Publicar
        if img_base64:
            st.write("🛠️ Aplicando marca y QR...")
            # Usamos la función que ya tenías para Base64
            url_final = aplicar_plantilla_y_texto_base64(img_base64, prod, frase_ia)
            
            if url_final:
                caption = f"✨ {frase_ia}\n\n🛍️ {prod['nombre'].upper()}\n🛒 {prod['url']}\n👉 ¡Escanea el QR para comprar!"
                publicar_en_instagram(url_final, caption, st.secrets["FB_ACCESS_TOKEN"], st.secrets["INSTAGRAM_ID"])
                st.success("✅ ¡Campaña publicada!")
        
        status.update(label="Proceso terminado", state="complete")

