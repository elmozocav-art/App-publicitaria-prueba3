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

# Control de automatización
if "ejecutando" not in st.session_state:
    st.session_state.ejecutando = False

col1, col2 = st.columns(2)
with col1:
    if st.button("🚀 Iniciar Modo Automático (Cada 20h)"):
        st.session_state.ejecutando = True
with col2:
    if st.button("🛑 Detener"):
        st.session_state.ejecutando = False

status_placeholder = st.empty()

while st.session_state.ejecutando:
    with st.status("🤖 Iniciando ciclo de publicación...", expanded=True) as status:
        # 1. Obtener producto real
        prod = obtener_producto_aleatorio_total()
        if not prod:
            prod = {"nombre": "DARPEPRO", "url": "https://darpepro.com"}

        # 2. Generar Imagen (Base64) - Sin frases de IA en el prompt de texto
        st.write(f"📸 Generando imagen para: {prod['nombre']}")
        img_base64 = None
        try:
            img_res = client.images.generate(
                model="gpt-image-1",
                prompt=f"Professional luxury studio photo of {prod['nombre']}, cinematic lighting",
                size="1024x1024",
                quality="high",
                response_format="b64_json" # Formato compatible con tu editor
            )
            img_base64 = img_res.data[0].b64_json
        except Exception as e:
            st.error(f"❌ Error API: {e}")

        # 3. Procesar y Publicar
        if img_base64:
            # Enviamos el nombre real del producto al editor
            url_final = aplicar_plantilla_y_texto_base64(img_base64, prod)
            
            if url_final:
                caption = f"🔥 Nuevo producto disponible: {prod['nombre'].upper()}\n\n🛒 Compra aquí: {prod['url']}"
                publicar_en_instagram(url_final, caption, st.secrets["FB_ACCESS_TOKEN"], st.secrets["INSTAGRAM_ID"])
                st.success(f"✅ Publicado: {prod['nombre']}")
        
        proxima_cita = datetime.now() + timedelta(hours=20)
        status.update(label=f"Próxima publicación: {proxima_cita.strftime('%H:%M:%S')}", state="complete")
    
    # Espera de 20 horas (72000 segundos)
    time.sleep(72000)
    st.rerun()
