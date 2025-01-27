import streamlit as st 
import requests
import os
import json  # Importar el módulo json

# Configuración de la página
st.set_page_config(
    page_title="🔤 Traductor Simple con DeepL API",
    page_icon="🔤",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Título y descripción
st.markdown(
    """
    <h1 style='text-align: center; color: #4B8BBE;'>🔤 Traductor Simple con DeepL API</h1>
    <p style='text-align: center;'>Traduce textos de manera rápida y eficiente entre múltiples idiomas.</p>
    """,
    unsafe_allow_html=True,
)

# Crear dos columnas para la entrada y la salida
col1, col2 = st.columns(2)

with col1:
    st.subheader("📄 Texto Original")
    texto_original = st.text_area(
        "Introduce el texto que deseas traducir:",
        height=300,
        placeholder="Escribe o pega el texto aquí..."
    )
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
    traduce = st.button("📝 Traducir")

with col2:
    st.subheader("📝 Texto Traducido")
    traduccion = ""
    if traduce:
        if texto_original.strip() == "":
            st.warning("⚠️ Por favor, introduce algún texto para traducir.")
        else:
            # Obtener la API Key desde los secrets de Streamlit
            API_KEY = st.secrets["DEEPL_API_KEY"]

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
                    st.success("✅ Traducción exitosa:")
                    st.write(traduccion)
                    
                    # Serializar el texto traducido para JavaScript
                    traduccion_json = json.dumps(traduccion)
                    
                    # Agregar el botón de copiar usando HTML y JavaScript
                    copy_button_html = f"""
                    <button onclick="copyToClipboard()" style="
                        background-color: #4B8BBE;
                        border: none;
                        color: white;
                        padding: 10px 20px;
                        text-align: center;
                        text-decoration: none;
                        display: inline-block;
                        font-size: 16px;
                        margin: 4px 2px;
                        cursor: pointer;
                        border-radius: 5px;
                    ">
                        📋 Copiar
                    </button>

                    <script>
                    function copyToClipboard() {{
                        const text = {traduccion_json};
                        navigator.clipboard.writeText(text).then(function() {{
                            alert('Texto copiado al portapapeles');
                        }}, function(err) {{
                            alert('Error al copiar el texto: ' + err);
                        }});
                    }}
                    </script>
                    """
                    
                    st.markdown(copy_button_html, unsafe_allow_html=True)
                else:
                    st.error("❌ No se encontró el campo 'translations' en la respuesta de la API.")
                    st.write(data)
            except requests.exceptions.HTTPError as http_err:
                st.error(f"❌ Error HTTP: {http_err}")
            except requests.exceptions.RequestException as req_err:
                st.error(f"❌ Error en la solicitud: {req_err}")
            except ValueError:
                st.error("❌ Error al decodificar la respuesta en formato JSON.")
    else:
        st.info("🔍 Introduce el texto y selecciona el idioma para comenzar la traducción.")

# Footer
st.markdown(
    """
    <hr>
    <p style='text-align: center;'>Desarrollado por <a href='https://github.com/tu_usuario'>Tu Nombre</a></p>
    """,
    unsafe_allow_html=True
)
