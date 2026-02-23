import streamlit as st
from darpe_scraper import obtener_producto_aleatorio_total
from editor_grafico import aplicar_plantilla_y_texto
from instagram_bot import publicar_en_instagram
from openai import OpenAI

# Configuración de la interfaz
st.set_page_config(page_title="DarpePro AI-Director", layout="centered")
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("🎬 Director Creativo DarpePro")

if st.button("🚀 Lanzar Campaña (Enlace Directo + Nombre Real)"):
    with st.status("🤖 Iniciando proceso creativo...", expanded=True) as status:
        
        # 1. SCRAPER: Obtener producto y su URL única
        st.write("🔍 Buscando producto en la tienda...")
        prod = obtener_producto_aleatorio_total()
        
        # Validamos que el scraper haya devuelto un enlace válido
        if not prod or "products" not in prod['url']:
            st.error("❌ No se pudo obtener un enlace directo. Reintenta.")
            st.stop()
            
        st.write(f"📦 Producto detectado: **{prod['nombre']}**")
        st.info(f"🔗 Enlace directo listo: {prod['url']}")

        # 2. GPT: Diseñar el escenario (Prohibimos texto en la imagen)
        st.write("🧠 GPT diseñando el concepto creativo...")
        diseño_ia = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Eres un director de arte publicitario. NO permitas texto en la imagen."},
                {"role": "user", "content": f"Diseña un escenario premium para '{prod['nombre']}'. FRASE: [5 palabras] | ESCENARIO: [ingles]"}
            ]
        )
        
        respuesta = diseño_ia.choices[0].message.content
        frase_ia = respuesta.split("|")[0].replace("FRASE:", "").strip()
        escenario_ia = respuesta.split("|")[1].replace("ESCENARIO:", "").strip()
        
        st.write(f"✨ Frase: *{frase_ia}*")

        # 3. DALL-E: Crear la fotografía publicitaria
        st.write("🎨 DALL-E ejecutando la fotografía...")
        prompt_final = (
            f"Professional high-end commercial photography of {prod['nombre']}. "
            f"Context: {escenario_ia}. Cinematic lighting, 8k, advertisement style. NO TEXT."
        )

        img_res = client.images.generate(model="dall-e-3", prompt=prompt_final)
        url_ia = img_res.data[0].url
        st.image(url_ia, caption="Imagen generada por IA")

        # 4. EDITOR Y PUBLICACIÓN: El enlace va directo al pie de foto
        st.write("🛠️ Aplicando plantilla y preparando post...")
        url_final = aplicar_plantilla_y_texto(url_ia, prod, frase_ia)

        if url_final:
            # Construcción del pie de foto con el LINK DIRECTO
            pie = (
                f"🔥 {prod['nombre']} \n"
                f"✨ {frase_ia} \n\n"
                f"🛍️ COMPRA DIRECTA AQUÍ: {prod['url']} \n\n"
                f"#DarpePro #TiendaOnline #Regalos"
            )
            
            # Publicamos en Instagram
            resultado = publicar_en_instagram(url_final, pie, st.secrets["FB_ACCESS_TOKEN"], st.secrets["INSTAGRAM_ID"])
            
            if isinstance(resultado, dict) and "id" in resultado:
                st.success(f"✅ ¡Publicado con éxito con su enlace directo!")
            else:
                st.error(f"❌ Error al publicar: {resultado}")
        
        status.update(label="✅ Proceso completado", state="complete")
