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
        # 1. SCRAPER: Obtenemos el producto y su imagen real
        prod = obtener_producto_aleatorio_total()
        st.write(f"📦 Producto detectado: **{prod['nombre']}**")

        # 2. GPT-3.5 ACTÚA COMO DIRECTOR DE ARTE (Crea el escenario y la frase)
        # Le pedimos que imagine un ambiente perfecto para ese producto específico
        st.write("🧠 GPT-3.5 diseñando el concepto creativo...")
        diseño_ia = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Eres un director de arte de fotografía publicitaria de lujo."},
                {"role": "user", "content": f"""
                    Para el producto '{prod['nombre']}', genera dos cosas:
                    1. Una frase de venta corta (5 palabras).
                    2. Una descripción detallada en inglés de un escenario fotográfico creativo y realista donde el producto luzca espectacular.
                    Responde en este formato: FRASE: [frase] | ESCENARIO: [escenario en ingles]
                """}
            ]
        )
        
        # Separamos la frase del escenario generado por la IA
        respuesta = diseño_ia.choices[0].message.content
        frase_ia = respuesta.split("|")[0].replace("FRASE:", "").strip()
        escenario_ia = respuesta.split("|")[1].replace("ESCENARIO:", "").strip()
        
        st.write(f"✨ Frase: *{frase_ia}*")
        st.write(f"🖼️ Escenario diseñado por IA: *{escenario_ia}*")

        # 3. DALL-E CREA LA IMAGEN BASADA EN EL DISEÑO ANTERIOR
        st.write("🎨 DALL-E ejecutando la fotografía...")
        prompt_final = (
            f"Professional high-end commercial photography. The product is {prod['nombre']}. "
            f"Reference look: {prod.get('imagen_real', '')}. "
            f"Context: {escenario_ia}. "
            f"Realistic textures, cinematic lighting, 8k resolution, advertisement style. No text."
        )

        img_res = client.images.generate(
            model="dall-e-3",
            prompt=prompt_final,
            size="1024x1024",
            quality="hd"
        )
        url_ia = img_res.data[0].url
        st.image(url_ia, caption="Imagen generada (Concepto IA)")

        # 4. MONTAJE Y PUBLICACIÓN
        # (Asegúrate de tener el editor_grafico.py con la función 'multiply' que te pasé antes)
        url_final = aplicar_plantilla_y_texto(url_ia, prod, frase_ia)

        if url_final:
            pie = (
                f"🔥 {prod['nombre']}\n\n"
                f"✨ {frase_ia}\n\n"
                f"🛒 Compra aquí:\n{prod['url']}\n\n"
                f"#DarpePro #Tecnologia #Oferta"
            )

            resultado = publicar_en_instagram(url_final, pie, st.secrets["FB_ACCESS_TOKEN"], st.secrets["INSTAGRAM_ID"])
            
            if isinstance(resultado, dict) and "id" in resultado:
                st.success("✅ ¡Publicado! La IA ha completado todo el ciclo creativo.")
            else:
                st.error(f"❌ Error: {resultado}")
        
        status.update(label="✅ Proceso completado", state="complete")

