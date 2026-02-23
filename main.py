import streamlit as st
from darpe_scraper import obtener_producto_aleatorio_total
from editor_grafico import aplicar_plantilla_y_texto
from instagram_bot import publicar_en_instagram
from openai import OpenAI

# Configuración de la página
st.set_page_config(page_title="DarpePro AI-Director v2", layout="centered")
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("🎬 Director Creativo DarpePro")

if st.button("🚀 Lanzar Campaña con Enlace Directo"):
    with st.status("🤖 Iniciando proceso creativo...", expanded=True) as status:
        
        # 1. SCRAPER: Obtenemos el producto y su URL específica
        st.write("🔍 Buscando producto en la tienda...")
        prod = obtener_producto_aleatorio_total()
        
        if not prod or prod['url'] == "https://darpepro.com":
            st.error("❌ No se pudo obtener un enlace directo. Reintenta.")
            st.stop()
            
        st.write(f"📦 Producto detectado: **{prod['nombre']}**")
        st.info(f"🔗 Enlace directo encontrado: {prod['url']}")

        # 2. GPT: DISEÑO DE ESCENARIO Y FRASE
        st.write("🧠 GPT diseñando el concepto visual...")
        diseño_ia = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Eres un director de arte de fotografía publicitaria. No permitas texto dentro de la imagen."},
                {"role": "user", "content": f"Para el producto '{prod['nombre']}', genera: 1. Frase de venta (5 palabras). 2. Escenario fotográfico en inglés. Formato: FRASE: [frase] | ESCENARIO: [escenario en ingles]"}
            ]
        )
        
        respuesta = diseño_ia.choices[0].message.content
        frase_ia = respuesta.split("|")[0].replace("FRASE:", "").strip()
        escenario_ia = respuesta.split("|")[1].replace("ESCENARIO:", "").strip()
        
        st.write(f"✨ Frase: *{frase_ia}*")

        # 3. DALL-E: GENERACIÓN DE LA IMAGEN
        st.write("🎨 DALL-E ejecutando la fotografía...")
        prompt_final = (
            f"Professional high-end commercial photography of {prod['nombre']}. "
            f"Context: {escenario_ia}. "
            f"Realistic textures, cinematic lighting, 8k, advertisement style. IMPORTANT: No text, no letters."
        )

        img_res = client.images.generate(
            model="dall-e-3",
            prompt=prompt_final,
            size="1024x1024"
        )
        url_ia = img_res.data[0].url
        st.image(url_ia, caption="Imagen Base (IA)")

        # 4. EDITOR Y PUBLICACIÓN
        st.write("🛠️ Aplicando plantilla y preparando post...")
        url_final = aplicar_plantilla_y_texto(url_ia, prod, frase_ia)

        if url_final:
            # Pie de foto con el enlace directo al producto
            pie = (
                f"🔥 {prod['nombre']} \n"
                f"✨ {frase_ia} \n\n"
                f"🛍️ COMPRA DIRECTA AQUÍ: {prod['url']} \n\n"
                f"#DarpePro #Ventas #Regalos"
            )
            
            resultado = publicar_en_instagram(url_final, pie, st.secrets["FB_ACCESS_TOKEN"], st.secrets["INSTAGRAM_ID"])
            
            if isinstance(resultado, dict) and "id" in resultado:
                st.success(f"✅ ¡Publicado con éxito!")
                st.write(f"Link del producto enviado a Instagram: {prod['url']}")
            else:
                st.error(f"❌ Error en Instagram: {resultado}")
        
        status.update(label="✅ Proceso completado", state="complete")
