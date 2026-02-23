import streamlit as st
from darpe_scraper import obtener_producto_aleatorio_total
from editor_grafico import aplicar_plantilla_y_texto
from instagram_bot import publicar_en_instagram
from openai import OpenAI

# Configuración inicial del Director Creativo
st.set_page_config(page_title="DarpePro AI-Director", layout="centered")
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("🎬 Director Creativo DarpePro")

if st.button("🚀 Lanzar Campaña (Enlace Directo + Nombre Real)"):
    with st.status("🤖 Iniciando proceso creativo...", expanded=True) as status:
        
        # 1. SCRAPER: Captura del producto y su link específico
        st.write("🔍 Buscando producto en la tienda...")
        prod = obtener_producto_aleatorio_total()
        
        # Verificación de seguridad para evitar errores de conexión
        if not prod or prod['url'] == "https://darpepro.com":
            st.error("❌ No se pudo obtener un enlace directo. Reintenta.") #
            st.stop()
            
        st.write(f"📦 Producto detectado: **{prod['nombre']}**")
        st.info(f"🔗 Enlace directo encontrado: {prod['url']}")

        # 2. GPT: Definición del concepto visual y frase
        st.write("🧠 GPT diseñando el concepto creativo...")
        diseño_ia = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Director de arte publicitario. NUNCA incluyas texto o letras en la imagen."},
                {"role": "user", "content": f"Diseña un escenario premium para el producto '{prod['nombre']}'. Formato: FRASE: [5 palabras] | ESCENARIO: [escenario en ingles]"}
            ]
        )
        
        respuesta = diseño_ia.choices[0].message.content
        frase_ia = respuesta.split("|")[0].replace("FRASE:", "").strip()
        escenario_ia = respuesta.split("|")[1].replace("ESCENARIO:", "").strip()
        
        st.write(f"✨ Frase: *{frase_ia}*")

        # 3. DALL-E: Creación de la fotografía publicitaria
        st.write("🎨 DALL-E ejecutando la fotografía...")
        prompt_final = (
            f"Professional high-end commercial photography of {prod['nombre']}. "
            f"Context: {escenario_ia}. "
            f"Realistic textures, cinematic lighting, 8k, advertisement style. NO TEXT, NO LETTERS."
        )

        img_res = client.images.generate(
            model="dall-e-3",
            prompt=prompt_final,
            size="1024x1024"
        )
        url_ia = img_res.data[0].url
        st.image(url_ia, caption="Fotografía generada por IA")

        # 4. EDITOR Y PUBLICACIÓN: Fusión con plantilla y enlace directo
        st.write("🛠️ Aplicando plantilla y preparando post...")
        url_final = aplicar_plantilla_y_texto(url_ia, prod, frase_ia)

        if url_final:
            # Construcción del pie de foto con el enlace directo
            pie = (
                f"🔥 {prod['nombre']} \n"
                f"✨ {frase_ia} \n\n"
                f"🛍️ COMPRA DIRECTA AQUÍ: {prod['url']} \n\n"
                f"#DarpePro #Novedades #TiendaOnline"
            )
            
            # Envío a Instagram
            resultado = publicar_en_instagram(url_final, pie, st.secrets["FB_ACCESS_TOKEN"], st.secrets["INSTAGRAM_ID"])
            
            if isinstance(resultado, dict) and "id" in resultado:
                st.success(f"✅ ¡Publicado con éxito con su enlace directo!")
            else:
                # Manejo de errores de publicación o timeout
                st.error(f"❌ Error en la publicación: {resultado}")
        
        status.update(label="✅ Proceso completado", state="complete")
