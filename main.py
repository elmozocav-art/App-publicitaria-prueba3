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

# Control de estado para el bucle
if "ejecutando" not in st.session_state:
    st.session_state.ejecutando = False

col1, col2 = st.columns(2)
with col1:
    if st.button("🚀 Iniciar Modo Automático (Cada 20h)"):
        st.session_state.ejecutando = True
with col2:
    if st.button("🛑 Detener"):
        st.session_state.ejecutando = False

if st.session_state.ejecutando:
    while st.session_state.ejecutando:
        with st.status("🤖 Procesando publicación automática...", expanded=True) as status:
            # 1. Obtener producto real
            prod = obtener_producto_aleatorio_total()
            if not prod:
                prod = {"nombre": "DarpePro Premium", "url": "https://darpepro.com"}

            # 2. Generar Imagen (Codificada Base64)
            # Eliminamos 'response_format' y 'background' para evitar el Error 400
            st.write(f"📸 Generando imagen para: {prod['nombre']}")
            img_base64 = None
            try:
                img_res = client.images.generate(
                    model="gpt-image-1",
                    prompt=f"Professional luxury studio photo of {prod['nombre']}, cinematic lighting",
                    size="1024x1024",
                    quality="high"
                )
                # Accedemos al contenido codificado que devuelve el modelo
                if img_res.data and hasattr(img_res.data[0], 'b64_json'):
                    img_base64 = img_res.data[0].b64_json
                else:
                    # Si el modelo devuelve b64 por defecto pero en otro campo
                    img_base64 = getattr(img_res.data[0], 'b64_json', None)
            except Exception as e:
                st.error(f"❌ Error API: {e}")

            # 3. Procesar y Publicar
            if img_base64:
                # Enviamos el nombre real para el diseño
                url_final = aplicar_plantilla_y_texto_base64(img_base64, prod)
                
                if url_final:
                    caption = f"🔥 {prod['nombre'].upper()}\n\n🛒 Compra aquí: {prod['url']}"
                    publicar_en_instagram(url_final, caption, st.secrets["FB_ACCESS_TOKEN"], st.secrets["INSTAGRAM_ID"])
                    st.success(f"✅ Publicado: {prod['nombre']}")
            
            proxima = datetime.now() + timedelta(hours=72000)
            status.update(label=f"Próxima publicación: {proxima.strftime('%H:%M:%S')}", state="complete")
        
        # Espera de 20 horas
        time.sleep(60)
        st.rerun()

