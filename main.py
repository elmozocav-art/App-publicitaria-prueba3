import streamlit as st
from darpe_scraper import obtener_producto_aleatorio_total
from editor_grafico import aplicar_plantilla_y_texto
from instagram_bot import publicar_en_instagram
from openai import OpenAI

# Configuración visual de la app
st.set_page_config(page_title="DarpePro Auto-Reel", layout="centered")

st.title("🎬 Generador de Reels DarpePro")
st.write("Crea anuncios verticales con IA y publícalos automáticamente.")

# Inicialización de OpenAI con tus credenciales seguras
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if st.button("🚀 Lanzar Campaña (Imagen + Frase IA)"):
    with st.status("🤖 El bot está trabajando...", expanded=True) as status:
        try:
            # --- PASO 1: SCRAPING ---
            st.write("🔍 Buscando producto en darpepro.com...")
            prod = obtener_producto_aleatorio_total()
            st.info(f"📦 Producto: **{prod['nombre']}**")

            # --- PASO 2: IA GENERA FRASE ---
            st.write("✍️ GPT escribiendo frase publicitaria...")
            gpt_res = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": f"Actúa como un experto en marketing. Escribe una frase corta e impactante (máximo 5 palabras) para vender este producto: {prod['nombre']}"}]
            )
            frase_ia = gpt_res.choices[0].message.content.strip('"')
            st.write(f"✨ Frase generada: *{frase_ia}*")

            # --- PASO 3: IA GENERA IMAGEN ---
            st.write("🎨 DALL-E creando imagen publicitaria...")
            img_res = client.images.generate(
                model="dall-e-3",
                prompt=f"Professional studio product photography of {prod['nombre']}, minimalist background, elegant cinematic lighting, 8k resolution",
                size="1024x1024"
            )
            url_ia = img_res.data[0].url
            st.image(url_ia, caption="Imagen original de la IA")

            # --- PASO 4: EDICIÓN CON PLANTILLA VERTICAL ---
            st.write("🖼️ Aplicando plantilla DarpePRO y textos...")
            # Esta función usa tu 'Plantilla DarpePRO.jpeg' y la sube a ImgBB
            url_final = aplicar_plantilla_y_texto(url_ia, prod, frase_ia)

            # --- PASO 5: PUBLICACIÓN EN INSTAGRAM ---
            if url_final:
                st.write("📲 Subiendo a Instagram como formato vertical...")
                
                # Creamos el pie de foto con el link directo que sacó el scraper
                pie = (
                    f"🔥 ¡NOVEDAD en DarpePro!\n\n"
                    f"⭐ {prod['nombre']}\n"
                    f"✨ {frase_ia}\n\n"
                    f"🔗 Consíguelo aquí: {prod['url']}\n\n"
                    f"#DarpePro #Tecnologia #Gadgets"
                )
                
                resultado = publicar_en_instagram(
                    url_final, 
                    pie, 
                    st.secrets["FB_ACCESS_TOKEN"].strip(), 
                    st.secrets["INSTAGRAM_ID"].strip()
                )
                
                if isinstance(resultado, dict) and "id" in resultado:
                    st.success(f"✅ ¡Publicado! ID del post: {resultado['id']}")
                else:
                    st.error(f"❌ Error al publicar: {resultado}")
            else:
                st.error("❌ No se pudo generar la imagen final.")

            status.update(label="✅ ¡Todo listo!", state="complete")

        except Exception as e:
            st.error(f"⚠️ Se detuvo el proceso: {e}")

