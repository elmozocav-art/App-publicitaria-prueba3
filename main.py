import streamlit as st
from darpe_scraper import obtener_producto_aleatorio_total
from editor_grafico import aplicar_plantilla_y_texto
from instagram_bot import publicar_en_instagram
from openai import OpenAI

st.set_page_config(page_title="DarpePro Bot v6", layout="centered")
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if st.button("🚀 Publicar Producto con Enlace Directo"):
    with st.status("🤖 Procesando...", expanded=True) as status:
        # A. SCRAPER: Obtenemos el link DIRECTO
        prod = obtener_producto_aleatorio_total()
        st.info(f"🔗 Enlace directo encontrado: {prod['url']}")

        # B. GPT: ESCENARIO Y FRASE
        diseño = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Director de arte. No permitas texto en la imagen."},
                {"role": "user", "content": f"Crea una frase de 5 palabras y un escenario en inglés para {prod['nombre']}. Formato: FRASE: [frase] | ESCENARIO: [escenario]"}
            ]
        )
        resp = diseño.choices[0].message.content
        frase_ia = resp.split("|")[0].replace("FRASE:", "").strip()
        escenario_ia = resp.split("|")[1].replace("ESCENARIO:", "").strip()

        # C. DALL-E: IMAGEN LIMPIA
        prompt_final = (
            f"Professional photography of {prod['nombre']}. Reference: {prod['imagen_real']}. "
            f"Context: {escenario_ia}. IMPORTANT: NO TEXT, NO LABELS, NO LETTERS. "
            f"Clean surfaces, 8k, cinematic lighting."
        )
        img_res = client.images.generate(model="dall-e-3", prompt=prompt_final, size="1024x1024")
        url_ia = img_res.data[0].url

        # D. EDITOR: Fusionar con plantilla (Usando multiply para quitar el blanco)
        url_final = aplicar_plantilla_y_texto(url_ia, prod, frase_ia)

        # E. PUBLICAR: Aquí va el enlace específico
        if url_final:
            pie = (
                f"🔥 {prod['nombre']} \n"
                f"✨ {frase_ia} \n\n"
                f"🔗 Link directo: {prod['url']} \n\n"
                f"#DarpePro #Ventas"
            )
            resultado = publicar_en_instagram(url_final, pie, st.secrets["FB_ACCESS_TOKEN"], st.secrets["INSTAGRAM_ID"])
            
            if isinstance(resultado, dict) and "id" in resultado:
                st.success("✅ ¡Publicado con éxito con su enlace directo!")
            else:
                st.error(f"❌ Error: {resultado}")
        
        status.update(label="✅ Proceso completado", state="complete")
