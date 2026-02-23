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

# ... (Tus imports y configuración inicial igual) ...

if st.button("🚀 Generar y Publicar Anuncio"):
    with st.status("Ejecutando proceso...", expanded=True) as status:
        try:
            # PASO A: Buscamos producto
            st.write("🔍 Buscando producto...")
            producto = obtener_producto_aleatorio_total()
            st.info(f"📦 Producto: {producto}")

            # PASO B: Generamos imagen con DALL-E
            st.write("🎨 Generando imagen con IA...")
            # (Aquí va tu código de client.images.generate...)
            url_ia = response.data[0].url 
            st.image(url_ia, caption="Imagen original (sin logo)")

            # PASO C: Edición y Subida a Hosting (NUEVO)
            st.write("🖼️ Añadiendo logo y creando enlace público...")
            # Esta función ahora nos devuelve la URL de ImgBB con el logo ya puesto
            url_final_con_logo = aplicar_marca_agua(url_ia, "logoDarpe.png")
            
            if url_final_con_logo:
                # PASO D: Instagram (CORREGIDO)
                st.write("📲 Subiendo a Instagram...")
                pie_de_foto = f"🚀 ¡Mira lo que tenemos hoy en Darpeshop! \n🔹 {producto} \n🛒 darpeshop.es"
                
                # ¡USAMOS url_final_con_logo!
                resultado = publicar_en_instagram(
                    url_final_con_logo, 
                    pie_de_foto, 
                    FB_ACCESS_TOKEN.strip(), 
                    INSTAGRAM_ID.strip()
                )
                
                st.success("✅ ¡Publicado en Instagram con éxito!")
                st.json(resultado)
            else:
                st.error("❌ Falló la creación de la imagen con logo.")

            status.update(label="✅ ¡Proceso completado!", state="complete")

        except Exception as e:
            st.error(f"Ocurrió un error: {e}")


