import streamlit as st
import time
from datetime import datetime, timedelta
from darpe_scraper import obtener_producto_aleatorio_total
from editor_grafico import aplicar_plantilla_y_texto
from instagram_bot import publicar_en_instagram
from openai import OpenAI

st.set_page_config(page_title="Director Automático DarpePro", layout="centered")
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("🎬 Director Automático DarpePro")

# Estado de la automatización
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
        # 1. Obtener producto real del scraper
        prod = obtener_producto_aleatorio_total()
        if not prod:
            prod = {"nombre": "DarpePro Premium", "url": "https://darpepro.com"}

        st.write(f"📦 Producto seleccionado: **{prod['nombre']}**")

        # 2. Generar Imagen (Sin parámetros conflictivos para evitar Error 400)
        st.write("📸 Generando imagen profesional...")
        url_ia = None
        try:
            # Eliminamos 'response_format' y 'background' para evitar el error 400
            img_res = client.images.generate(
                model="gpt-image-1",
                prompt=f"Professional luxury studio photo of {prod['nombre']}, cinematic lighting",
                size="1024x1024",
                quality="high"
            )
            
            if img_res.data and img_res.data[0].url:
                url_ia = img_res.data[0].url
                st.write("✅ Imagen recibida correctamente.")
            else:
                st.error("⚠️ OpenAI no devolvió una URL válida.")
                
        except Exception as e:
            st.error(f"❌ Error API: {e}")

        # 3. Procesar y Publicar
        if url_ia:
            st.write("🛠️ Aplicando marca y QR...")
            # Pasamos solo el producto para poner su nombre real y el QR
            url_final = aplicar_plantilla_y_texto(url_ia, prod)
            
            if url_final:
                caption = f"🔥 {prod['nombre'].upper()}\n\n🛒 Disponible aquí: {prod['url']}"
                publicar_en_instagram(url_final, caption, st.secrets["FB_ACCESS_TOKEN"], st.secrets["INSTAGRAM_ID"])
                st.success(f"✅ Publicado con éxito: {prod['nombre']}")
        
        proxima = datetime.now() + timedelta(hours=20)
        status.update(label=f"Próxima publicación: {proxima.strftime('%H:%M:%S')}", state="complete")
    
    # Espera de 20 horas (72.000 segundos)
    time.sleep(72000)
    st.rerun()
