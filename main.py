import streamlit as st
import random
from darpe_scraper import obtener_producto_aleatorio_total
from editor_grafico import aplicar_plantilla_y_texto
from instagram_bot import publicar_en_instagram
from openai import OpenAI

st.set_page_config(page_title="DarpePro Auto-Ads", layout="centered")
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Lista de ambientes para que la IA varíe el estilo
ESCENARIOS = [
    "on a luxury dark marble table with soft warm spotlight",
    "in a futuristic cyberpunk showroom with blue and pink neon reflections",
    "on a clean minimalist white wooden desk with a plant in the background",
    "floating in a premium 3D studio with soft cinematic shadows",
    "in a high-tech modern office with a blurred window view"
]

st.title("🎬 Generador de Reels DarpePro")

if st.button("🚀 Crear Anuncio Profesional"):
    with st.status("Generando contenido...", expanded=True) as status:
        # A. SCRAPER: Trae nombre y la URL de la FOTO REAL
        prod = obtener_producto_aleatorio_total()
        st.write(f"📦 Producto real detectado: {prod['nombre']}")
        
        # B. IA: FRASE DE VENTA
        gpt_res = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": f"Frase publicitaria de 5 palabras para: {prod['nombre']}"}]
        )
        frase = gpt_res.choices[0].message.content.strip('"')

        # C. IA: IMAGEN BASADA EN EL PRODUCTO REAL
        ambiente = random.choice(ESCENARIOS)
        # Usamos la imagen real como referencia en el prompt
        prompt_ia = (
            f"Professional high-end product photography. The product is a {prod['nombre']}. "
            f"Reference look: {prod.get('imagen_real', '')}. "
            f"Place the product {ambiente}. Realistic textures, 8k resolution, "
            f"commercial advertising style. No text, no extra logos."
        )
        
        st.write("🎨 DALL-E creando escenario variable...")
        img_res = client.images.generate(
            model="dall-e-3",
            prompt=prompt_ia,
            size="1024x1024",
            quality="hd"
        )
        url_ia = img_res.data[0].url
        st.image(url_ia, caption="Imagen generada por IA")

        # D. MONTAJE: Combinar fondo IA con Plantilla DarpePro
        url_final = aplicar_plantilla_y_texto(url_ia, prod, frase)

        # E. INSTAGRAM: Publicación con pausa de seguridad
        if url_final:
            pie = f"🔥 {prod['nombre']} \n✨ {frase} \n🔗 Compra aquí: {prod['url']}"
            resultado = publicar_en_instagram(url_final, pie, st.secrets["FB_ACCESS_TOKEN"], st.secrets["INSTAGRAM_ID"])
            
            if isinstance(resultado, dict) and "id" in resultado:
                st.success("✅ ¡Publicado en Instagram con éxito!")
            else:
                st.error(f"❌ Error en publicación: {resultado}")
        
        status.update(label="✅ Proceso terminado", state="complete")
