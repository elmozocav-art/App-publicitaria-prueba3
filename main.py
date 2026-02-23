# PASO A: Scraper mejorado
st.write("🔍 Rastreando DarpePro en busca de novedades...")
producto_info = obtener_producto_aleatorio_total() # Ahora devuelve {'nombre': '...', 'url': '...'}

producto_nombre = producto_info['nombre']
producto_url = producto_info['url']

st.info(f"📦 Producto seleccionado: **{producto_nombre}**")

# ... (PASO B: Generar imagen con IA usando el producto_nombre) ...

# PASO C: Edición con la nueva plantilla
# Usamos la plantilla vertical que subiste
url_final_con_logo = aplicar_plantilla_y_texto(url_ia, producto_info)

if url_final_con_logo:
    # PASO D: Publicación con Link Directo
    pie_de_foto = (
        f"🚀 ¡Novedad en DarpePro!\n\n"
        f"🔹 {producto_nombre}\n"
        f"🔥 Consíguelo aquí: {producto_url}\n\n"
        f"#DarpePro #Tecnologia #Oferta"
    )
    
    # Publicar...
