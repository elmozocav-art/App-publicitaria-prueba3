import streamlit as st
from darpe_scraper import obtener_producto_aleatorio_total
from editor_grafico import aplicar_plantilla_y_texto
from openai import OpenAI

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if st.button("🚀 Lanzar Campaña"):
    with st.spinner("Conectando con la tienda..."):
        prod = obtener_producto_aleatorio_total()
        
        if prod:
            st.success(f"📦 Producto: {prod['nombre']}")
            
            # Generar imagen con DALL-E (Sin texto para evitar errores)
            img_res = client.images.generate(
                model="dall-e-3",
                prompt=f"Premium product photography of {prod['nombre']} in a clean studio, 8k, no text.",
            )
            url_ia = img_res.data[0].url
            
            # Crear post final
            url_final = aplicar_plantilla_y_texto(url_ia, prod, "OFERTA")
            
            if url_final:
                st.image(url_final)
                st.info(f"🔗 Enlace directo listo: {prod['url']}")
        else:
            st.error("Fallo de conexión. Inténtalo de nuevo en unos segundos.")
