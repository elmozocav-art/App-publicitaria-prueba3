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
        try:
            # PASO A: Scraping
            st.write("🔍 Buscando producto en Darpeshop...")
            producto = obtener_producto_aleatorio_total()
            st.info(f"📦 Producto seleccionado: **{producto}**")

            # PASO B: Generación de Imagen
            st.write("🎨 Generando imagen publicitaria...")
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
            
            # PASO C: Edición
            st.write("🖼️ Añadiendo marca de agua...")
            archivo_final = aplicar_marca_agua(url_ia, "logoDarpe.png")
            
            # PASO D: Instagram
            if archivo_final:
                st.write("📲 Subiendo a Instagram...")
                pie_de_foto = f"🚀 ¡Mira lo que tenemos hoy en Darpeshop! \n🔹 {producto} \n🛒 darpeshop.es #tecnologia"
                
                # Publicar (Token y luego ID)
                resultado = publicar_en_instagram(url_ia, pie_de_foto, FB_ACCESS_TOKEN.strip(), INSTAGRAM_ID.strip())
                
                if isinstance(resultado, dict) and "error" in resultado:
                    st.error("❌ Error de Instagram/Facebook")
                else:
                    st.success("✅ ¡Proceso de envío completado!")
                
                st.json(resultado)
            
            status.update(label="✅ ¡Terminado!", state="complete")

        except Exception as e:
            st.error(f"❌ Error: {e}")


