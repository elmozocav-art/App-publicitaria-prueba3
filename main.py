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

        # 1️⃣ Producto
        prod = obtener_producto_aleatorio_total()
        if not prod:
            prod = {"nombre": "Producto DarpePro", "url": "https://darpepro.com"}

        # 2️⃣ Texto GPT-4o
        frase_ia = "Diseño que marca la diferencia"
        escenario_ia = "High-end product photography, minimalist luxury"
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

        # 3️⃣ Imagen GPT-Image-1 (Calidad High + Base64)
        st.write("📸 Generando imagen técnica...")
        img_base64 = None
        try:
            # Según el video: gpt-image-1 no usa URL, usa b64_json
            img_res = client.images.generate(
                model="gpt-image-1",
                prompt=f"Official studio photo of {prod['nombre']}, {escenario_ia}, 8k resolution.",
                size="1024x1024",
                quality="high", # Valor correcto según logs
                response_format="b64_json" # Forzamos el formato Base64 visto en el video
            )
            img_base64 = img_res.data[0].b64_json
            st.write("✅ Imagen generada correctamente.")
        except Exception as e:
            st.error(f"❌ Error en la IA de imagen: {e}")

        # 4️⃣ Procesamiento Final y Publicación
        if img_base64:
            st.write("🛠️ Aplicando QR y marca DarpePro...")
            url_final = aplicar_plantilla_y_texto_base64(img_base64, prod, frase_ia)
            
            if url_final:
                # Caption optimizada con enlace limpio
                caption = (
                    f"🔥 {prod['nombre'].upper()}\n"
                    f"✨ {frase_ia}\n\n"
                    f"🛒 Consíguelo aquí: {prod['url']}\n"
                    f"📲 O escanea el QR de la imagen!"
                )
                
                publicar_en_instagram(
                    url_final, 
                    caption, 
                    st.secrets["FB_ACCESS_TOKEN"], 
                    st.secrets["INSTAGRAM_ID"]
                )
                st.success("✅ Campaña publicada con éxito.")
            else:
                st.error("❌ Fallo en la creación del post final.")
        
        status.update(label="Campaña Finalizada", state="complete")
