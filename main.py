import streamlit as st
from darpe_scraper import obtener_producto_aleatorio_total
from editor_grafico import aplicar_plantilla_y_texto
from instagram_bot import publicar_en_instagram
from openai import OpenAI

st.set_page_config(page_title="DarpePro AI-Director", layout="centered")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("🎬 Director Creativo DarpePro")

if st.button("🚀 Generar Campaña Inteligente"):

    with st.status("🤖 IA trabajando...", expanded=True) as status:

        # 1️⃣ Obtener producto
        prod = obtener_producto_aleatorio_total()

        st.write(f"📦 Producto detectado: **{prod['nombre']}**")
        st.write(f"🔗 Enlace detectado: {prod['url']}")

        # 2️⃣ Generar frase + escenario
        diseño_ia = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "Eres un director creativo experto en publicidad premium."
                },
                {
                    "role": "user",
                    "content": f"""
Para el producto '{prod['nombre']}':

1. Crea una frase corta (máximo 5 palabras).
2. Describe un escenario fotográfico profesional en inglés.

Formato:
FRASE: texto | ESCENARIO: texto
"""
                }
            ]
        )

        respuesta = diseño_ia.choices[0].message.content

        try:
            frase_ia = respuesta.split("|")[0].replace("FRASE:", "").strip()
            escenario_ia = respuesta.split("|")[1].replace("ESCENARIO:", "").strip()
        except:
            frase_ia = "Innovación sin límites"
            escenario_ia = "Modern studio lighting, premium commercial look"

        st.write(f"✨ Frase: {frase_ia}")

        # 3️⃣ Generar imagen
        prompt_final = (
            f"Professional high-end commercial photography. "
            f"The product is {prod['nombre']}. "
            f"{escenario_ia}. "
            f"Ultra realistic, cinematic lighting, 8k resolution. No text."
        )

        img_res = client.images.generate(
            model="dall-e-3",
            prompt=prompt_final,
            size="1024x1024",
            quality="hd"
        )

        url_ia = img_res.data[0].url
        st.image(url_ia)

        # 4️⃣ Aplicar plantilla
        url_final = aplicar_plantilla_y_texto(url_ia, prod, frase_ia)

        if not url_final:
            st.error("Error generando imagen final.")
            st.stop()

        # 5️⃣ Crear caption con enlace directo
        caption = (
            f"🔥 {prod['nombre']}\n\n"
            f"✨ {frase_ia}\n\n"
            f"🛒 Compra aquí:\n"
            f"{prod['url']}\n\n"
            f"#DarpePro #Tecnologia #Ofertas"
        )

        # 6️⃣ Publicar
        resultado = publicar_en_instagram(
            url_final,
            caption,
            st.secrets["FB_ACCESS_TOKEN"],
            st.secrets["INSTAGRAM_ID"]
        )

        if isinstance(resultado, dict) and "id" in resultado:
            st.success("✅ ¡Publicado correctamente!")
        else:
            st.error(f"Error al publicar: {resultado}")

        status.update(label="✅ Proceso completado", state="complete")
