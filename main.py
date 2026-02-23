import streamlit as st
from darpe_scraper import obtener_producto_aleatorio_total
from editor_grafico import aplicar_plantilla_y_texto
from instagram_bot import publicar_en_instagram
from openai import OpenAI

st.set_page_config(page_title="DarpePro AI-Director", layout="centered")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("🎬 Director Creativo DarpePro")

if st.button("🚀 Generar Campaña Inteligente"):

    with st.status("🤖 IA analizando producto y diseñando escenario...", expanded=True) as status:

        # 1️⃣ OBTENER PRODUCTO
        prod = obtener_producto_aleatorio_total()

        # 🔴 VALIDACIÓN IMPORTANTE
        if not prod:
            st.error("❌ No se pudo obtener un producto válido.")
            st.stop()

        st.write(f"📦 Producto detectado: **{prod['nombre']}**")
        st.write(f"🔗 Enlace detectado: {prod['url']}")

        # 2️⃣ GPT CREA FRASE Y ESCENARIO
        st.write("🧠 IA diseñando el concepto creativo...")

        diseño_ia = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "Eres un director de arte de fotografía publicitaria de lujo."
                },
                {
                    "role": "user",
                    "content": f"""
Para el producto '{prod['nombre']}', genera:

1. Una frase de venta corta (máximo 5 palabras).
2. Una descripción detallada en inglés de un escenario fotográfico realista.

Formato exacto de respuesta:
FRASE: [frase] | ESCENARIO: [escenario]
"""
                }
            ]
        )

        respuesta = diseño_ia.choices[0].message.content

        try:
            frase_ia = respuesta.split("|")[0].replace("FRASE:", "").strip()
            escenario_ia = respuesta.split("|")[1].replace("ESCENARIO:", "").strip()
        except:
            st.error("❌ Error interpretando respuesta de la IA.")
            st.stop()

        st.write(f"✨ Frase: *{frase_ia}*")
        st.write(f"🖼️ Escenario IA: *{escenario_ia}*")

        # 3️⃣ GENERAR IMAGEN CON DALL·E
        st.write("🎨 Generando imagen publicitaria...")

        prompt_final = (
            f"Professional high-end commercial photography. "
            f"The product is {prod['nombre']}. "
            f"Context: {escenario_ia}. "
            f"Ultra realistic, cinematic lighting, 8k resolution, advertisement style. No text."
        )

        img_res = client.images.generate(
            model="dall-e-3",
            prompt=prompt_final,
            size="1024x1024",
            quality="hd"
        )

        url_ia = img_res.data[0].url
        st.image(url_ia, caption="Imagen generada por IA")

        # 4️⃣ EDITAR IMAGEN CON PLANTILLA
        url_final = aplicar_plantilla_y_texto(url_ia, prod, frase_ia)

        if not url_final:
            st.error("❌ Error generando imagen final.")
            st.stop()

        # 5️⃣ CREAR CAPTION CON ENLACE DIRECTO AL PRODUCTO
        caption = (
            f"🔥 {prod['nombre']}\n\n"
            f"✨ {frase_ia}\n\n"
            f"🛒 Compra aquí:\n"
            f"{prod['url']}\n\n"
            f"#DarpePro #Tecnologia #Ofertas"
        )

        # 6️⃣ PUBLICAR EN INSTAGRAM
        resultado = publicar_en_instagram(
            url_final,
            caption,
            st.secrets["FB_ACCESS_TOKEN"],
            st.secrets["INSTAGRAM_ID"]
        )

        if isinstance(resultado, dict) and "id" in resultado:
            st.success("✅ ¡Publicado correctamente!")
        else:
            st.error(f"❌ Error al publicar: {resultado}")

        status.update(label="✅ Proceso completado", state="complete")

