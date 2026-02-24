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
        if not prod:
            st.error("No se pudo conectar con la web. Revisa el scraper.")
            st.stop()

        st.write(f"📦 Producto: **{prod['nombre']}**")

        # 2️⃣ Generar Prompt Maestro (GPT-4o para máxima calidad de texto)
        diseño_ia = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Eres un Director Creativo experto en fotografía publicitaria de lujo."},
                {"role": "user", "content": f"Producto: {prod['nombre']}. Crea: 1. Frase de venta (5 palabras). 2. Descripción técnica detallada para IA de imagen (estilo premium, 85mm, cinematic lighting, ultra-realistic). Formato: FRASE: texto | ESCENARIO: texto"}
            ]
        )
        
        respuesta = diseño_ia.choices[0].message.content
        try:
            frase_ia = respuesta.split("|")[0].replace("FRASE:", "").strip()
            escenario_ia = respuesta.split("|")[1].replace("ESCENARIO:", "").strip()
        except Exception as e:
            st.warning(f"Aviso en GPT: {e}. Usando valores por defecto.")
            frase_ia = "Excelencia en cada detalle"
            escenario_ia = "High-end commercial photography, minimalist studio, soft shadows"

        st.write(f"✨ Frase: {frase_ia}")

        # 3️⃣ Generar Imagen con GPT Image 1 (SOLUCIÓN AL ERROR 400)
        st.write("📸 Generando imagen con GPT Image 1...")
        
        prompt_final = (
            f"Official commercial studio photography of {prod['nombre']}. "
            f"Concept: {escenario_ia}. Hyper-realistic textures, professional color grading, "
            f"sharp focus, 8k resolution, clean composition. NO text."
        )

        try:
            # CORRECCIÓN: Ajuste de 'quality' según los logs de error
            img_res = client.images.generate(
                model="gpt-image-1", 
                prompt=prompt_final,
                size="1024x1024",
                quality="high" # Se cambia 'hd' por 'high' que es el valor soportado
            )
            
            if img_res and img_res.data:
                url_ia = img_res.data[0].url
                st.image(url_ia, caption="Generado con GPT Image 1")
            else:
                st.error("La IA no devolvió ninguna imagen.")
                st.stop()
        except Exception as e:
            st.error(f"Error crítico en el modelo de imagen: {e}")
            st.stop()

        # 4️⃣ Procesamiento Final y Publicación
        st.write("🛠️ Aplicando diseño DarpePro...")
        url_final = aplicar_plantilla_y_texto(url_ia, prod, frase_ia)

        if url_final:
            caption = f"🔥 {prod['nombre'].upper()}\n\n✨ {frase_ia}\n\n🛒 Compra aquí: {prod['url']}\n\n#DarpePro #IA #TechStyle"
            
            resultado = publicar_en_instagram(
                url_final,
                caption,
                st.secrets["FB_ACCESS_TOKEN"],
                st.secrets["INSTAGRAM_ID"]
            )

            if isinstance(resultado, dict) and "id" in resultado:
                st.success("✅ ¡Campaña publicada con éxito!")
            else:
                st.error("Error al publicar en Instagram.")

        status.update(label="✅ Proceso completado", state="complete")
