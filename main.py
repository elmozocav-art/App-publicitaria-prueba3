import streamlit as st
from darpe_scraper import obtener_producto_aleatorio_total
from editor_grafico import aplicar_marca_agua
from instagram_bot import publicar_en_instagram
from openai import OpenAI
import os

# 1. Configuración de página
st.set_page_config(page_title="Darpe Bot", layout="centered")

st.title("🤖 Generador Publicitario Darpe")
st.write("Haz clic en el botón de abajo para iniciar la magia.")

# 2. Credenciales (Limpiadas y verificadas)
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
INSTAGRAM_ID = st.secrets["INSTAGRAM_ID"]
FB_ACCESS_TOKEN = st.secrets["FB_ACCESS_TOKEN"]
# Inicializamos el cliente usando la variable directamente
client = OpenAI(api_key=OPENAI_API_KEY)

# --- INTERFAZ DE USUARIO ---

if st.button("🚀 Generar y Publicar Anuncio"):
    with st.status("Ejecutando proceso...", expanded=True) as status:
        
        # PASO A: Scraping
        st.write("🔍 Buscando producto en Darpeshop...")
        producto = obtener_producto_aleatorio_total()
        st.info(f"📦 Producto seleccionado: **{producto}**")

        # PASO B: Generación de Imagen con DALL-E 3
        st.write("🎨 Generando imagen publicitaria con OpenAI...")
        try:
            prompt_publicidad = f"Professional advertising photography of {producto}, clean background, cinematic lighting, 8k resolution, high-end tech product style."
            
            response = client.images.generate(
                model="dall-e-3",
                prompt=prompt_publicidad,
                size="1024x1024",
                quality="hd",
                n=1,
            )
            url_ia = response.data[0].url
            st.image(url_ia, caption="Imagen generada por IA")
            
            # PASO C: Edición - Poner el logo de Darpeshop
            st.write("🖼️ Añadiendo marca de agua...")
            archivo_final = aplicar_marca_agua(url_ia, "logoDarpe.png")
            
            # PASO D: Instagram - Publicar
            if archivo_final:
                st.write("📲 Subiendo a Instagram...")
                pie_de_foto = f"🚀 ¡Mira lo que tenemos hoy en Darpeshop! \n🔹 {producto} \n🛒 darpeshop.es #tecnologia #oferta"
                
                # Publicar
                resultado = publicar_en_instagram(url_ia, pie_de_foto, FB_ACCESS_TOKEN, INSTAGRAM_ID)
                st.success(f"✅ ¡Publicado con éxito!")
                st.json(resultado)
            
            status.update(label="✅ ¡Proceso terminado!", state="complete")

        except Exception as e:
            st.error(f"❌ Error: {e}")
            st.info("💡 Si el error persiste, verifica el saldo en platform.openai.com/billing")

















