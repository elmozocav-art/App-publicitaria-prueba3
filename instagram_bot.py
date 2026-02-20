import requests

def publicar_en_instagram(image_url, caption, access_token, instagram_id):
    """
    Publica una imagen en Instagram usando la API de Graph.
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