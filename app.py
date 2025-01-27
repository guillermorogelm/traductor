import streamlit as st
import requests

# Configuración de la página
st.set_page_config(
    page_title="Traductor con DeepL",
    page_icon="🔤",
    layout="centered",
    initial_sidebar_state="auto",
)

# Título de la aplicación
st.title("🔤 Traductor Simple con DeepL API")

# Descripción
st.write("""
Este es un traductor simple que utiliza la API de DeepL para traducir textos entre diferentes idiomas.
""")

# Entrada de texto
texto_original = st.text_area("Introduce el texto que deseas traducir:", height=200)

# Selección de idioma de destino
idiomas_disponibles = {
    "Español": "ES",
    "Inglés": "EN",
    "Francés": "FR",
    "Alemán": "DE",
    "Italiano": "IT",
    "Portugués": "PT",
    "Holandés": "NL",
    "Polaco": "PL",
    "Ruso": "RU",
    "Chino": "ZH",
    # Agrega más idiomas según tus necesidades
}

idioma_destino = st.selectbox("Selecciona el idioma de destino:", list(idiomas_disponibles.keys()))

# Botón de traducción
if st.button("Traducir"):
    if texto_original.strip() == "":
        st.warning("Por favor, introduce algún texto para traducir.")
    else:
        # Configura tu clave de API de DeepL
        API_KEY = "d056980c-2647-48d7-a55b-779d098bc7a2:fx"

        # Endpoint para la API gratuita de DeepL
        url = "https://api-free.deepl.com/v2/translate"

        # Parámetros de la solicitud
        params = {
            "auth_key": API_KEY,
            "text": texto_original,
            "target_lang": idiomas_disponibles[idioma_destino]
        }

        # Hacer la solicitud POST a la API de DeepL
        try:
            response = requests.post(url, data=params)
            response.raise_for_status()  # Lanza una excepción si la respuesta fue un error

            data = response.json()

            if "translations" in data:
                traduccion = data["translations"][0]["text"]
                st.success("**Traducción:**")
                st.write(traduccion)
            else:
                st.error("No se encontró el campo 'translations' en la respuesta de la API.")
                st.write(data)
        except requests.exceptions.HTTPError as http_err:
            st.error(f"Error HTTP: {http_err}")
        except requests.exceptions.RequestException as req_err:
            st.error(f"Error en la solicitud: {req_err}")
        except ValueError:
            st.error("Error al decodificar la respuesta en formato JSON.")
