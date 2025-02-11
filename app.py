import streamlit as st
import requests

# Configuración de la página
st.set_page_config(
    page_title="🔤 Traductor DeepL",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Encabezado con diseño elegante
st.markdown("""
    <div style="background-color: #4B8BBE; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
        <h1 style="color: white; text-align: center;">Traductor DeepL</h1>
        <p style="color: white; text-align: center; font-size: 18px;">Traduce textos de forma rápida y eficiente</p>
    </div>
    """, unsafe_allow_html=True)

# Crear dos columnas: izquierda para entrada y derecha para salida
col_input, col_output = st.columns(2)

# Columna de entrada
with col_input:
    st.subheader("Texto Original")
    texto_original = st.text_area(
        "Ingresa el texto que deseas traducir:",
        height=300,
        placeholder="Escribe o pega tu texto aquí..."
    )
    st.markdown("**Selecciona el idioma de destino:**")
    # Diccionario de idiomas (códigos de DeepL)
    idiomas = {
        "Español": "ES",
        "Inglés": "EN",
        "Francés": "FR",
        "Alemán": "DE",
        "Italiano": "IT",
        "Portugués": "PT",
        "Holandés": "NL",
        "Polaco": "PL",
        "Ruso": "RU",
        "Chino": "ZH"
    }
    idioma_destino = st.selectbox("Elige el idioma de destino:", list(idiomas.keys()))
    traducir_btn = st.button("📝 Traducir")

# Columna de salida
with col_output:
    st.subheader("Texto Traducido")
    if traducir_btn:
        if texto_original.strip() == "":
            st.warning("⚠️ Por favor, ingresa un texto para traducir.")
        else:
            # Obtener la API Key de DeepL de los secrets de Streamlit
            API_KEY = st.secrets["DEEPL_API_KEY"]
            
            # Endpoint y parámetros de la solicitud
            url = "https://api-free.deepl.com/v2/translate"
            params = {
                "auth_key": API_KEY,
                "text": texto_original,
                "target_lang": idiomas[idioma_destino]
            }
            
            try:
                response = requests.post(url, data=params)
                response.raise_for_status()  # Verifica si hubo error HTTP
                data = response.json()
                
                if "translations" in data:
                    traduccion = data["translations"][0]["text"]
                    st.success("✅ Traducción exitosa:")
                    # Mostramos la traducción dentro de un cuadro con fondo claro
                    st.markdown(f"""
                        <div style="background-color: #e6f7ff; padding: 15px; border-radius: 8px; font-size: 16px;">
                            {traduccion}
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.error("❌ No se encontró la traducción en la respuesta de la API.")
                    st.write(data)
            except requests.exceptions.HTTPError as errh:
                st.error(f"❌ Error HTTP: {errh}")
            except requests.exceptions.RequestException as errr:
                st.error(f"❌ Error en la solicitud: {errr}")
            except Exception as e:
                st.error(f"❌ Ocurrió un error: {e}")
    else:
        st.info("🔍 Ingresa el texto y selecciona el idioma para comenzar la traducción.")

# Footer
st.markdown("""
    <hr>
    <p style="text-align: center;">Desarrollado por <a href="https://github.com/tu_usuario" target="_blank">Tu Nombre</a></p>
    """, unsafe_allow_html=True)
