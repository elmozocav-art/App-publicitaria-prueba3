import requests
import time  # <--- Añadimos esto
import streamlit as st # Para mostrar el mensaje en la web

def publicar_en_instagram(image_url, caption, access_token, instagram_id):
    """
    Publica una imagen en Instagram usando la API de Graph con tiempo de espera.
    """
    # Paso 1: Subir la imagen al contenedor de Meta
    post_url = f"https://graph.facebook.com/v19.0/{instagram_id}/media"
    payload = {
        'image_url': image_url,
        'caption': caption,
        'access_token': access_token
    }
    
    response = requests.post(post_url, data=payload)
    result = response.json()
    
    if 'id' in result:
        creation_id = result['id']
        
        # --- NUEVA MODIFICACIÓN ---
        # Avisamos en Streamlit y esperamos para que Meta procese la imagen
        st.write("⏳ Instagram está procesando la imagen de ImgBB. Esperando 30 segundos...")
        time.sleep(30) # <--- Esta pausa evita el error de Media ID
        # --------------------------

        # Paso 2: Publicar el contenedor creado
        publish_url = f"https://graph.facebook.com/v19.0/{instagram_id}/media_publish"
        publish_payload = {
            'creation_id': creation_id,
            'access_token': access_token
        }
        publish_response = requests.post(publish_url, data=publish_payload)
        return publish_response.json()
    else:
        return result
