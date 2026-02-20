import streamlit as st
from darpe_scraper import obtener_producto_aleatorio_total
from editor_grafico import aplicar_marca_agua
from instagram_bot import publicar_en_instagram
from openai import OpenAI
import os

# 1. Configuración de página (SIEMPRE PRIMERO)
st.set_page_config(page_title="Darpe Bot", layout="centered")

st.title("🤖 Generador Publicitario Darpe")
st.write("Haz clic en el botón de abajo para iniciar la magia.")

# 2. Configuración de Credenciale
OPENAI_API_KEY = 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
INSTAGRAM_ID = 17841480726721041
FB_ACCESS_TOKEN = IGAAMHxUfIVolBZAFpvdkdiTUdFdDZAnTFM3akhTUW4tdnpfSkxCQjhkci1xdkxCNml1eV80V2lrd2pCb2ZAheUZApUUMzQ21uU2c5TW9GdXh3aDZAIbEU2bmJZATUlKMk1KVXBCSC0zQ0FuNnlSQVZAvdThNa09EZAHczNmp3aFRIeExGOAZDZD

client = OpenAI(api_key= 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

# --- INTERFAZ DE USUARIO ---

if st.button("🚀 Generar y Publicar Anuncio"):
    # Usamos un contenedor de estado para que el usuario vea qué está pasando
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
            
            # Mostramos la imagen generada en la web
            st.image(url_ia, caption="Imagen generada por IA")
            
            # PASO C: Edición - Poner el logo de Darpeshop
            st.write("🖼️ Añadiendo marca de agua...")
            archivo_final = aplicar_marca_agua(url_ia, "logoDarpe.png")
            
            # PASO D: Instagram - Publicar
            if archivo_final:
                st.write("📲 Subiendo a Instagram...")
                pie_de_foto = f"🚀 ¡Mira lo que tenemos hoy en Darpeshop! \n🔹 {producto} \n🛒 Encuéntralo en darpeshop.es #tecnologia #oferta"
                
                # IMPORTANTE: Usamos la URL de la IA directamente si no tienes hosting para el archivo final
                resultado = publicar_en_instagram(url_ia, pie_de_foto, FB_ACCESS_TOKEN, INSTAGRAM_ID)
                
                st.success(f"✅ ¡Publicado con éxito!")
                st.json(resultado)
            
            status.update(label="✅ ¡Proceso terminado!", state="complete")

        except Exception as e:
            st.error(f"❌ Error: {e}")
            st.info("💡 Revisa los logs o tu saldo en OpenAI.")




