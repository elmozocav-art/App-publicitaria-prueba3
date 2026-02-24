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

        # 1️⃣ Obtener Producto
        prod = obtener_producto_aleatorio_total()
        if not prod:
            prod = {"nombre": "Producto DarpePro", "url": "https://darpepro.com"}

        # 2️⃣ Texto GPT-4o
        frase_ia = "Innovación que cautiva"
        escenario_ia = "Luxury product photography, studio background"
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
            st.warning("⚠️ Usando textos de reserva.")

        # 3️⃣ Generar Imagen (FORMATO BASE64 PARA DESENCRIPTAR)
        st.write("📸 Generando imagen (Datos Base64)...")
        img_b64 = None
        try:
            img_res = client.images.generate(
                model="gpt-image-1",
                prompt=f"Professional photo of {prod['nombre']}, {escenario_ia}",
                size="1024x1024",
                quality="high", 
                response_format="b64_json" # <--- ESTO ES LO QUE PIDE EL VIDEO
            )
            
            # Extraemos los datos encriptados en lugar de la URL
            if img_res.data and img_res.data[0].b64_json:
                img_b64 = img_res.data[0].b64_json
                st.write("✅ Datos de imagen recibidos.")
            else:
                st.error("⚠️ OpenAI no devolvió datos Base64 válidos.")
        except Exception as e:
            st.error(f"❌ Error en la API: {e}")

        # 4️⃣ Procesar y Publicar (Solo si tenemos los datos b64)
        if img_b64:
            st.write("🛠️ Desencriptando y aplicando marca...")
            url_final = aplicar_plantilla_y_texto_base64(img_b64, prod, frase_ia)
            
            if url_final:
                caption = f"🔥 {prod['nombre'].upper()}\n✨ {frase_ia}\n🛒 {prod['url']}\n\n#DarpePro #PublicidadIA"
                publicar_en_instagram(url_final, caption, st.secrets["FB_ACCESS_TOKEN"], st.secrets["INSTAGRAM_ID"])
                st.success("✅ ¡Campaña publicada con éxito!")
            else:
                st.error("❌ El editor falló al procesar los datos desencriptados.")
        
        status.update(label="Proceso terminado", state="complete")
