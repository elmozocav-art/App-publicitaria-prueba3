import streamlit as st
from darpe_scraper import obtener_producto_aleatorio_total
from editor_grafico import aplicar_plantilla_y_texto
from instagram_bot import publicar_en_instagram
from openai import OpenAI

st.set_page_config(page_title="DarpePro Auto-Reel", layout="centered")
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("🎬 Generador de Reels DarpePro")

if st.button("🚀 Lanzar Campaña (Imagen Realista)"):
    with st.status("🤖 Generando contenido premium...", expanded=True) as status:
        try:
            # 1. SCRAPING
            prod = obtener_producto_aleatorio_total()
            st.info(f"📦 Producto seleccionado: **{prod['nombre']}**")

            # 2. IA GENERA FRASE
            gpt_res = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": f"Eres un experto en marketing de lujo. Escribe una frase corta (máx 5 palabras) para: {prod['nombre']}"}]
            )
            frase_ia = gpt_res.choices[0].message.content.strip('"')

            # 3. IA GENERA IMAGEN (PROMPT MEJORADO PARA REALISMO)
            st.write("🎨 Creando fotografía de catálogo...")
            # Forzamos estilo fotográfico comercial, sin texto y con luz real
            prompt_pro = (
                f"High-end professional commercial photography of {prod['nombre']}. "
                f"Clean studio lighting, bokeh background, realistic textures, 8k resolution, "
                f"advertising style, sharp focus. No drawings, no distorted text."
            )
            
            img_res = client.images.generate(
                model="dall-e-3",
                prompt=prompt_pro,
                size="1024x1024",
                quality="hd" # Calidad superior
            )
            url_ia = img_res.data[0].url
            st.image(url_ia, caption="Fotografía base de la IA")

            # 4. EDICIÓN INTEGRADA
            url_final = aplicar_plantilla_y_texto(url_ia, prod, frase_ia)

            # 5. PUBLICACIÓN
            if url_final:
                pie = f"🔥 ¡Novedad en DarpePro! \n⭐ {prod['nombre']}\n✨ {frase_ia}\n🔗 {prod['url']}"
                resultado = publicar_en_instagram(url_final, pie, st.secrets["FB_ACCESS_TOKEN"], st.secrets["INSTAGRAM_ID"])
                
                if isinstance(resultado, dict) and "id" in resultado:
                    st.success(f"✅ ¡Publicado con éxito!")
                else:
                    st.error(f"❌ Error en IG: {resultado}")
            
            status.update(label="✅ ¡Campaña finalizada!", state="complete")

        except Exception as e:
            st.error(f"⚠️ Error general: {e}")
