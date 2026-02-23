import streamlit as st
from darpe_scraper import obtener_producto_aleatorio_total
from editor_grafico import aplicar_plantilla_y_texto
from instagram_bot import publicar_en_instagram
from openai import OpenAI

st.set_page_config(page_title="DarpePro Bot v7", layout="centered")
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if st.button("🚀 Lanzar Campaña con Enlace Directo"):
    with st.status("🔍 Extrayendo datos reales de la web...", expanded=True) as status:
        # A. SCRAPER
        prod = obtener_producto_aleatorio_total()
        
        if not prod or "url" not in prod:
            st.error("❌ No se pudo extraer un enlace directo. Revisa el Scraper.")
            status.update(label="Fallo en la extracción", state="error")
            st.stop()

        st.success(f"📦 Producto: {prod['nombre']}")
        st.info(f"🔗 Enlace Directo: {prod['url']}")

        # B. GPT: ESCENARIO Y FRASE
        # Forzamos a que NO use la palabra "Producto"
        diseño = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Eres un creativo publicitario. NUNCA escribas texto dentro de la imagen."},
                {"role": "user", "content": f"Crea una frase de 5 palabras y un escenario en inglés para el producto: {prod['nombre']}. Formato: FRASE: [frase] | ESCENARIO: [escenario]"}
            ]
        )
        resp = diseño.choices[0].message.content
        frase_ia = resp.split("|")[0].replace("FRASE:", "").strip()
        escenario_ia = resp.split("|")[1].replace("ESCENARIO:", "").strip()

        # C. DALL-E: IMAGEN SIN TEXTO
        prompt_final = (
            f"Professional photography of {prod['nombre']}. Context: {escenario_ia}. "
            f"IMPORTANT: DO NOT INCLUDE ANY TEXT, LABELS OR LOGOS. "
            f"Focus on the product design, 8k, realistic."
        )
        img_res = client.images.generate(model="dall-e-3", prompt=prompt_final)
        url_ia = img_res.data[0].url

        # D. EDITOR: Escribe el NOMBRE REAL y quita el blanco de la plantilla
        url_final = aplicar_plantilla_y_texto(url_ia, prod, frase_ia)

        # E. PUBLICAR: Usando la URL específica del producto
        if url_final:
            pie_de_foto = (
                f"🔥 {prod['nombre']} \n"
                f"✨ {frase_ia} \n\n"
                f"🔗 Disponible aquí: {prod['url']} \n\n"
                f"#DarpePro #Tecnologia #Gadgets"
            )
            
            res_ig = publicar_en_instagram(url_final, pie_de_foto, st.secrets["FB_ACCESS_TOKEN"], st.secrets["INSTAGRAM_ID"])
            
            if "id" in res_ig:
                st.success(f"✅ ¡Publicado! Link: {prod['url']}")
            else:
                st.error(f"❌ Error IG: {res_ig}")
        
        status.update(label="✅ Proceso completado", state="complete")
