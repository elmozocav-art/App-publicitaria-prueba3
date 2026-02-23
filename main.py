import streamlit as st
import random
from darpe_scraper import obtener_producto_aleatorio_total
from editor_grafico import aplicar_plantilla_y_texto
from instagram_bot import publicar_en_instagram
from openai import OpenAI

st.set_page_config(page_title="DarpePro AI-Director v5", layout="centered")
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("🎬 Director Creativo DarpePro")

if st.button("🚀 Generar y Publicar con Enlace Directo"):
    with st.status("🤖 IA analizando producto y generando contenido...", expanded=True) as status:
        # 1. SCRAPER: Obtenemos el producto con su URL y FOTO REAL
        prod = obtener_producto_aleatorio_total()
        st.write(f"📦 Producto: **{prod['nombre']}**")
        st.write(f"🔗 Enlace detectado: {prod['url']}")

        # 2. GPT: DISEÑO DE ESCENARIO (Sin permitir texto en la imagen)
        diseño_ia = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Eres un director de arte de fotografía de producto. No incluyas NUNCA texto o etiquetas en la imagen."},
                {"role": "user", "content": f"Diseña un escenario de lujo para {prod['nombre']}. Responde: FRASE: [frase 5 palabras] | ESCENARIO: [escenario en ingles]"}
            ]
        )
        
        respuesta = diseño_ia.choices[0].message.content
        frase_ia = respuesta.split("|")[0].replace("FRASE:", "").strip()
        escenario_ia = respuesta.split("|")[1].replace("ESCENARIO:", "").strip()

        # 3. DALL-E: IMAGEN LIMPIA (Prohibición estricta de la palabra 'PRODUCTO')
        prompt_final = (
            f"Professional high-end commercial photography of {prod['nombre']}. "
            f"Reference visual: {prod.get('imagen_real', '')}. "
            f"Context: {escenario_ia}. "
            f"IMPORTANT: NO TEXT, NO LABELS, NO LETTERS, NO TYPOGRAPHY. Clean product surface. "
            f"8k resolution, cinematic lighting."
        )

        img_res = client.images.generate(
            model="dall-e-3",
            prompt=prompt_final,
            size="1024x1024",
            quality="hd"
        )
        url_ia = img_res.data[0].url
        st.image(url_ia, caption="Imagen generada (Limpia)")

        # 4. EDITOR: Montaje y escritura del nombre REAL por código
        url_final = aplicar_plantilla_y_texto(url_ia, prod, frase_ia)

        # 5. PUBLICACIÓN: Con el enlace directo al producto
        if url_final:
            # Aquí usamos prod['url'] que viene del scraper
            pie = (
                f"🔥 ¡NUEVA LLEGADA! \n\n"
                f"⭐ {prod['nombre']} \n"
                f"✨ {frase_ia} \n\n"
                f"🔗 Cómpralo aquí: {prod['url']} \n\n"
                f"#DarpePro #Tecnologia #Oferta"
            )
            
            resultado = publicar_en_instagram(url_final, pie, st.secrets["FB_ACCESS_TOKEN"], st.secrets["INSTAGRAM_ID"])
            
            if isinstance(resultado, dict) and "id" in resultado:
                st.success(f"✅ ¡Publicado con éxito! Enlace directo: {prod['url']}")
            else:
                st.error(f"❌ Error en IG: {resultado}")
        
        status.update(label="✅ Proceso completado", state="complete")
