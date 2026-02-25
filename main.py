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

# Control de estado para el bucle infinito
if "bot_activo" not in st.session_state:
    st.session_state.bot_activo = False

col1, col2 = st.columns(2)
with col1:
    if st.button("🚀 Iniciar Automatización (20h)"):
        st.session_state.bot_activo = True
with col2:
    if st.button("🛑 Detener Bot"):
        st.session_state.bot_activo = False

if st.session_state.bot_activo:
    while st.session_state.bot_activo:
        with st.status("🤖 Procesando publicación...", expanded=True) as status:
            # 1. Obtener producto y su imagen real desde el scraper
            prod = obtener_producto_aleatorio_total()
            if not prod:
                prod = {"nombre": "Producto DarpePro", "url": "https://darpepro.com", "imagen_url": ""}

            st.write(f"📦 Producto detectado: {prod['nombre']}")

            # 2. Generar Imagen Basada en la Realidad
            # NO usamos 'response_format' ni 'background' para evitar el Error 400
            img_base64 = None
            try:
                # Prompt mejorado para que la IA se base en la URL de la imagen del producto
                prompt_ia = (
                    f"Create a professional luxury commercial photo for {prod['nombre']}. "
                    f"Base the design on this product: {prod.get('imagen_url', '')}. "
                    f"Cinematic studio lighting, minimalist background. "
                    f"IMPORTANT: NO TEXT, NO LOGOS, NO LETTERS ON THE PRODUCT."
                )
                
                img_res = client.images.generate(
                    model="gpt-image-1",
                    prompt=prompt_ia,
                    size="1024x1024",
                    quality="high"
                )
                
                # Acceso seguro al contenido Base64
                if img_res.data:
                    img_base64 = getattr(img_res.data[0], 'b64_json', None)
            except Exception as e:
                st.error(f"❌ Error API: {e}")

            # 3. Procesar con Editor y Publicar
            if img_base64:
                # Pasamos el producto completo para usar su NOMBRE REAL y su URL en el QR
                url_final = aplicar_plantilla_y_texto_base64(img_base64, prod)
                
                if url_final:
                    caption = f"🔥 {prod['nombre'].upper()}\n\n🛒 Disponible aquí: {prod['url']}"
                    publicar_en_instagram(url_final, caption, st.secrets["FB_ACCESS_TOKEN"], st.secrets["INSTAGRAM_ID"])
                    st.success(f"✅ Publicado con éxito: {prod['nombre']}")
            
            proxima = datetime.now() + timedelta(hours=20)
            status.update(label=f"Próxima publicación: {proxima.strftime('%H:%M:%S')}", state="complete")
        
        # Pausa de 20 horas [72000 segundos]
        time.sleep(72000)
        st.rerun()
