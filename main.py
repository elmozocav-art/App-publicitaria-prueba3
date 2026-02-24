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

        # 1️⃣ Obtener Producto
        prod = obtener_producto_aleatorio_total()
        if not prod:
            # Respaldo si el scraper falla
            prod = {"nombre": "DarpePro Premium", "url": "https://darpepro.com"}

        # 2️⃣ Texto GPT-4o
        frase_ia = "Excelencia en cada detalle"
        escenario_ia = "Luxury product photography, studio background"
        try:
            diseño_ia = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": f"Producto: {prod['nombre']}. Crea FRASE: (5 palabras) | ESCENARIO: (inglés)."}]
            )
            res = diseño_ia.choices[0].message.content
            if "|" in res:
                frase_ia = res.split("|")[0].replace("FRASE:", "").strip()
                escenario_ia = res.split("|")[1].replace("ESCENARIO:", "").strip()
        except Exception as e:
            st.warning(f"⚠️ Aviso en GPT: {e}. Usando valores por defecto.")

        # 3️⃣ Generar Imagen (CORRECCIÓN ERROR 400 Y NONETYPE)
        st.write("📸 Generando imagen profesional...")
        url_ia = None
        try:
            # Eliminamos 'response_format' que causaba el Error 400
            img_res = client.images.generate(
                model="gpt-image-1",
                prompt=f"Professional photo of {prod['nombre']}, {escenario_ia}",
                size="1024x1024",
                quality="high" # Valor correcto según tus logs
            )
            
            # Solo asignamos si la respuesta es exitosa para evitar el 'NoneType'
            if img_res.data and img_res.data[0].url:
                url_ia = img_res.data[0].url
                st.write("✅ Imagen generada exitosamente.")
            else:
                st.error("⚠️ OpenAI no devolvió una URL válida.")
        except Exception as e:
            st.error(f"❌ Error en la IA de imagen: {e}")

        # 4️⃣ Solo procedemos si tenemos una imagen válida
        if url_ia:
            st.write("🛠️ Aplicando QR y marca...")
            url_final = aplicar_plantilla_y_texto(url_ia, prod, frase_ia)
            
            if url_final:
                caption = (
                    f"✨ {frase_ia}\n\n"
                    f"🛍️ Producto: {prod['nombre'].upper()}\n"
                    f"🛒 Consíguelo aquí: {prod['url']}\n"
                    f"👉 Escanea el QR en la foto para comprar al instante!"
                )
                
                publicar_en_instagram(
                    url_final, 
                    caption, 
                    st.secrets["FB_ACCESS_TOKEN"], 
                    st.secrets["INSTAGRAM_ID"]
                )
                st.success("✅ Campaña publicada con enlace y QR")
            else:
                st.error("❌ El editor no pudo generar la imagen final.")
        
        status.update(label="Proceso terminado", state="complete")
