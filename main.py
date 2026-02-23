import streamlit as st
from darpe_scraper import obtener_producto_aleatorio_total
from editor_grafico import aplicar_plantilla_y_texto
from instagram_bot import publicar_en_instagram
from openai import OpenAI

# Configuración de página y cliente
st.set_page_config(page_title="DarpePro AI-Director", layout="centered")
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("🎬 Director Creativo DarpePro")

if st.button("🚀 Lanzar Campaña (Enlace Directo + Nombre Real)"):
    # Usamos st.status para agrupar los pasos y dar feedback visual
    with st.status("🤖 Iniciando proceso creativo...", expanded=True) as status:
        
        # 1. SCRAPER: Obtención del producto y su URL
        st.write("🔍 Buscando producto en la tienda...")
        prod = obtener_producto_aleatorio_total()
        
        # Validación de seguridad: Si falla el scraper, detenemos para no publicar basura
        if not prod or prod['url'] == "https://darpepro.com":
            st.error("❌ Error de conexión: No se pudo obtener un enlace directo.")
            st.stop()
            
        st.write(f"📦 Producto detectado: **{prod['nombre']}**")
        st.info(f"🔗 Enlace directo listo: {prod['url']}")

        # 2. GPT: Creación del concepto publicitario
        st.write("🧠 GPT analizando el producto...")
        diseño_ia = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Director de arte publicitario. Prohibido incluir texto o letras en la imagen."},
                {"role": "user", "content": f"Crea un escenario premium para '{prod['nombre']}'. Formato: FRASE: [5 palabras] | ESCENARIO: [ingles]"}
            ]
        )
        
        respuesta = diseño_ia.choices[0].message.content
        frase_ia = respuesta.split("|")[0].replace("FRASE:", "").strip()
        escenario_ia = respuesta.split("|")[1].replace("ESCENARIO:", "").strip()
        
        st.write(f"✨ Frase: *{frase_ia}*")

        # 3. DALL-E: Fotografía publicitaria
        st.write("🎨 DALL-E ejecutando la fotografía...")
        prompt_final = (
            f"Professional high-end commercial photography of {prod['nombre']}. "
            f"Context: {escenario_ia}. Realistic textures, cinematic lighting, 8k, advertisement style. NO TEXT."
        )

        img_res = client.images.generate(model="dall-e-3", prompt=prompt_final)
        url_ia = img_res.data[0].url
        st.image(url_ia, caption="Base generada por IA")

        # 4. MONTAJE Y PUBLICACIÓN FINAL
        st.write("🛠️ Aplicando plantilla y preparando post...")
        url_final = aplicar_plantilla_y_texto(url_ia, prod, frase_ia)

        if url_final:
            # PIE DE FOTO: Aquí insertamos el ENLACE DIRECTO dinámicamente
            pie = (
                f"🔥 {prod['nombre']} \n"
                f"✨ {frase_ia} \n\n"
                f"🛍️ COMPRA DIRECTA AQUÍ: {prod['url']} \n\n"
                f"#DarpePro #Ventas #MarketingIA"
            )
            
            # Ejecución de la publicación en Instagram
            resultado = publicar_en_instagram(url_final, pie, st.secrets["FB_ACCESS_TOKEN"], st.secrets["INSTAGRAM_ID"])
            
            if isinstance(resultado, dict) and "id" in resultado:
                st.success("✅ ¡Campaña publicada con éxito!")
                st.balloons()
            else:
                # Manejo de errores de red o API de Facebook
                st.error(f"❌ Error al publicar en Instagram: {resultado}")
        
        status.update(label="✅ Proceso completado", state="complete")
