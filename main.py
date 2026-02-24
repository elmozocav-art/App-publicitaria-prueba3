import streamlit as st
import time
from datetime import datetime, timedelta
from darpe_scraper import obtener_producto_aleatorio_total
from editor_grafico import aplicar_plantilla_y_texto_base64
from instagram_bot import publicar_en_instagram
from openai import OpenAI

st.set_page_config(page_title="DarpePro Auto-Bot", layout="centered")
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("🎬 Director Automático DarpePro")

if "bot_activo" not in st.session_state:
    st.session_state.bot_activo = False

col1, col2 = st.columns(2)
with col1:
    if st.button("🚀 Iniciar Automatización (20h)"):
        st.session_state.bot_activo = True
with col2:
    if st.button("🛑 Detener Bot"):
        st.session_state.bot_activo = False

while st.session_state.bot_activo:
    with st.status("🤖 Ciclo activo...", expanded=True) as status:
        # 1. Obtener producto real
        prod = obtener_producto_aleatorio_total() or {"nombre": "DarpePro Premium", "url": "https://darpepro.com"}

        # 2. Generar Imagen (Base64)
        # Sin 'response_format' ni 'background' para evitar el Error 400
        st.write(f"📸 Generando imagen para: {prod['nombre']}")
        img_base64 = None
        try:
            img_res = client.images.generate(
                model="gpt-image-1",
                prompt=f"Professional luxury photo of {prod['nombre']}, studio background",
                size="1024x1024",
                quality="high"
            )
            # Extraemos los datos codificados según tu modelo
            if img_res.data:
                img_base64 = getattr(img_res.data[0], 'b64_json', None)
        except Exception as e:
            st.error(f"❌ Error API: {e}")

        # 3. Procesar y Publicar
        if img_base64:
            # Enviamos el producto para usar su NOMBRE REAL en el diseño
            url_final = aplicar_plantilla_y_texto_base64(img_base64, prod)
            
            if url_final:
                caption = f"🔥 {prod['nombre'].upper()}\n\n🛒 Compra aquí: {prod['url']}"
                publicar_en_instagram(url_final, caption, st.secrets["FB_ACCESS_TOKEN"], st.secrets["INSTAGRAM_ID"])
                st.success(f"✅ Publicado: {prod['nombre']}")
        
        proxima = datetime.now() + timedelta(hours=20)
        status.update(label=f"Próxima publicación: {proxima.strftime('%H:%M:%S')}", state="complete")
    
    time.sleep(72000) # Espera exacta de 20 horas
    st.rerun()
