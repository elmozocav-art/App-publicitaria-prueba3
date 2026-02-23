import streamlit as st
from darpe_scraper import obtener_producto_aleatorio_total
from editor_grafico import aplicar_plantilla_y_texto
from instagram_bot import publicar_en_instagram
from openai import OpenAI

st.set_page_config(page_title="DarpePro Auto-Reel v9", layout="centered")
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if st.button("🚀 Lanzar Campaña (Enlace Directo + Nombre Real)"):
    with st.status("🔗 Conectando con la base de datos de DarpePro...", expanded=True) as status:
        prod = obtener_producto_aleatorio_total()
        
        if not prod:
            st.error("❌ No se pudieron obtener productos. Reintenta en 5 segundos.")
            status.update(label="Fallo de conexión", state="error")
            st.stop()

        st.success(f"📦 Producto: **{prod['nombre']}**")
        st.info(f"🔗 Enlace: {prod['url']}")

        # GPT: Crea el Escenario
        diseño = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Director de arte. NUNCA menciones letras o texto en tus descripciones."},
                {"role": "user", "content": f"Diseña un escenario premium para {prod['nombre']}. FRASE: [5 palabras] | ESCENARIO: [ingles]"}
            ]
        )
        resp = diseño.choices[0].message.content
        frase_ia = resp.split("|")[0].replace("FRASE:", "").strip()
        escenario_ia = resp.split("|")[1].replace("ESCENARIO:", "").strip()

        # DALL-E: Foto Limpia (Sin palabras como 'PRODUCTO')
        prompt_final = (
            f"Commercial photography of {prod['nombre']}. {escenario_ia}. "
            f"STRICTLY NO TEXT, NO LETTERS, NO LABELS. Clean product surfaces. 8k resolution."
        )
        img_res = client.images.generate(model="dall-e-3", prompt=prompt_final)
        url_ia = img_res.data[0].url
        st.image(url_ia, caption="Fondo generado por IA (Sin texto)")

        # EDITOR: Python escribe el NOMBRE REAL sobre la imagen
        url_final = aplicar_plantilla_y_texto(url_ia, prod, frase_ia)

        if url_final:
            pie = f"🔥 {prod['nombre']} \n✨ {frase_ia} \n\n🔗 {prod['url']}"
            res_ig = publicar_en_instagram(url_final, pie, st.secrets["FB_ACCESS_TOKEN"], st.secrets["INSTAGRAM_ID"])
            
            if "id" in res_ig:
                st.success("✅ ¡Publicado con éxito con su enlace directo!")
            else:
                st.error(f"❌ Error: {res_ig}")
        
        status.update(label="✅ Proceso completado", state="complete")
