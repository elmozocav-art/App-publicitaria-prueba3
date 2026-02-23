import streamlit as st
from darpe_scraper import obtener_producto_aleatorio_total
from editor_grafico import aplicar_plantilla_y_texto
from instagram_bot import publicar_en_instagram
from openai import OpenAI

st.set_page_config(page_title="DarpePro Bot v8", layout="centered")
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if st.button("🚀 Lanzar Campaña con Enlace Directo"):
    with st.status("🔍 Conectando con la tienda...", expanded=True) as status:
        # A. SCRAPER
        prod = obtener_producto_aleatorio_total()
        
        if prod is None:
            st.error("❌ La web de DarpePro no respondió o no se encontraron productos. Inténtalo de nuevo en unos segundos.")
            status.update(label="Error de conexión", state="error")
            st.stop()

        st.success(f"📦 Producto: **{prod['nombre']}**")
        st.info(f"🔗 Link Directo: {prod['url']}")

        # B. IA CREATIVA (Genera Frase y Escenario)
        diseño = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Director de arte publicitario. NUNCA escribas texto en la imagen."},
                {"role": "user", "content": f"Diseña un escenario premium para {prod['nombre']}. FRASE: [5 palabras] | ESCENARIO: [en ingles]"}
            ]
        )
        resp = diseño.choices[0].message.content
        frase_ia = resp.split("|")[0].replace("FRASE:", "").strip()
        escenario_ia = resp.split("|")[1].replace("ESCENARIO:", "").strip()

        # C. DALL-E (Imagen Limpia)
        prompt_final = (
            f"High-end photography of {prod['nombre']}. {escenario_ia}. "
            f"NO TEXT, NO LABELS, NO LETTERS. Professional lighting, 8k."
        )
        img_res = client.images.generate(model="dall-e-3", prompt=prompt_final)
        url_ia = img_res.data[0].url

        # D. EDITOR (Escribe el nombre real y une la plantilla)
        url_final = aplicar_plantilla_y_texto(url_ia, prod, frase_ia)

        # E. INSTAGRAM (Pie de foto con el enlace correcto)
        if url_final:
            pie = f"🔥 {prod['nombre']} \n✨ {frase_ia} \n\n🔗 {prod['url']}"
            res_ig = publicar_en_instagram(url_final, pie, st.secrets["FB_ACCESS_TOKEN"], st.secrets["INSTAGRAM_ID"])
            
            if "id" in res_ig:
                st.success("✅ ¡Publicado con éxito!")
            else:
                st.error(f"❌ Error Instagram: {res_ig}")
        
        status.update(label="✅ Proceso completado", state="complete")
