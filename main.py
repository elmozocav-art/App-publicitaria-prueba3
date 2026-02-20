from darpe_scraper import obtener_producto_aleatorio_total
from editor_grafico import aplicar_marca_agua
from instagram_bot import publicar_en_instagram
from openai import OpenAI
import os

# 1. Configuración de Credenciales
# Reemplaza con tus claves reales
OPENAI_API_KEY = "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" 
INSTAGRAM_ID = "17841480726721041"
FB_ACCESS_TOKEN = "IGAAMHxUfIVolBZAFpvdkdiTUdFdDZAnTFM3akhTUW4tdnpfSkxCQjhkci1xdkxCNml1eV80V2lrd2pCb2ZAheUZApUUMzQ21uU2c5TW9GdXh3aDZAIbEU2bmJZATUlKMk1KVXBCSC0zQ0FuNnlSQVZAvdThNa09EZAHczNmp3aFRIeExGOAZDZD"

client = OpenAI(api_key="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")


def ejecutar_bot_openai():
    # PASO A: Scraping - Elegir producto de Darpeshop
    print("🔍 Buscando producto en la web...")
    producto = obtener_producto_aleatorio_total() #
    print(f"📦 Producto seleccionado: {producto}")

    # PASO B: Generación de Imagen con DALL-E 3
    print("🎨 Generando imagen publicitaria con OpenAI...")
    try:
        prompt_publicidad = f"Professional advertising photography of {producto}, clean background, cinematic lighting, 8k resolution, high-end tech product style."
        
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt_publicidad,
            size="1024x1024",
            quality="hd",
            n=1,
        )
        url_ia = response.data[0].url
        
        # PASO C: Edición - Poner el logo de Darpeshop
        print("🖼️ Añadiendo identidad de marca...")
        archivo_final = aplicar_marca_agua(url_ia, "logoDarpe.png")
        
        # PASO D: Instagram - Publicar
        if archivo_final:
            # Importante: Para que Instagram lo vea, la imagen debe estar en una URL pública
            # Si usas Streamlit Cloud, la URL sería: https://tu-app.streamlit.app/post_final.png
            url_publica_imagen = "https://tu-app.streamlit.app/post_final.png" 
            pie_de_foto = f"🚀 ¡Mira lo que tenemos hoy en Darpeshop! \n🔹 {producto} \n🛒 Encuéntralo en darpeshop.es #tecnologia #oferta"
            
            print("📲 Subiendo a Instagram...")
            resultado = publicar_en_instagram(url_publica_imagen, pie_de_foto, INSTAGRAM_ID, FB_ACCESS_TOKEN)
            print(f"✅ Resultado: {resultado}")

    except Exception as e:
        print(f"❌ Error en el proceso de OpenAI: {e}")
        print("💡 Nota: Revisa si tienes saldo cargado en platform.openai.com/billing")

if __name__ == "__main__":
    ejecutar_bot_openai()