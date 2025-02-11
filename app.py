import streamlit as st
import requests

# Configuración de la página
st.set_page_config(
    page_title="Guillermo's Translator",
    layout="wide",
    page_icon=":speech_balloon:"
)

# Estilos personalizados para imitar un diseño similar a DeepL
st.markdown("""
    <style>
    /* Estilo global */
    body {
        background-color: #f2f2f2;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    /* Título principal */
    .title {
        font-size: 3em;
        text-align: center;
        margin-bottom: 0.5em;
        color: #2c3e50;
    }
    /* Encabezados de cada panel */
    .panel-title {
        font-size: 1.5em;
        color: #2c3e50;
        margin-bottom: 0.2em;
    }
    /* Texto descriptivo pequeño */
    .small-text {
        font-size: 0.9em;
        color: gray;
        margin-bottom: 1em;
    }
    /* Estilos para el área de texto de entrada */
    .stTextArea textarea {
        border: 1px solid #dfe6e9;
        border-radius: 5px;
        padding: 10px;
        font-size: 1em;
        background-color: #ffffff;
        box-shadow: 0px 2px 5px rgba(0,0,0,0.1);
    }
    /* Estilos para el contenedor de salida (traducción) */
    .output-box {
        border: 1px solid #dfe6e9;
        border-radius: 5px;
        padding: 10px;
        font-size: 1em;
        min-height: 300px;
        background-color: #ffffff;
        box-shadow: inset 0px 2px 5px rgba(0,0,0,0.05);
    }
    /* Estilo para el botón */
    div.stButton > button {
        background-color: #2c3e50;
        color: white;
        border: none;
        border-radius: 5px;
        padding: 10px 20px;
        font-size: 1em;
        margin-top: 20px;
    }
    div.stButton > button:hover {
        background-color: #34495e;
    }
    </style>
    """, unsafe_allow_html=True)

# Título de la aplicación
st.markdown("<div class='title'>Guillermo's Translator</div>", unsafe_allow_html=True)

# Diccionario con todos los idiomas soportados por la API de DeepL
idiomas = {
    "Búlgaro (BG)": "BG",
    "Checo (CS)": "CS",
    "Danés (DA)": "DA",
    "Alemán (DE)": "DE",
    "Griego (EL)": "EL",
    "Inglés (EN)": "EN",
    "Español (ES)": "ES",
    "Estonio (ET)": "ET",
    "Finlandés (FI)": "FI",
    "Francés (FR)": "FR",
    "Húngaro (HU)": "HU",
    "Indonesio (ID)": "ID",
    "Italiano (IT)": "IT",
    "Japonés (JA)": "JA",
    "Lituano (LT)": "LT",
    "Letón (LV)": "LV",
    "Holandés (NL)": "NL",
    "Polaco (PL)": "PL",
    "Portugués (PT-PT)": "PT-PT",
    "Portugués (PT-BR)": "PT-BR",
    "Rumano (RO)": "RO",
    "Ruso (RU)": "RU",
    "Eslovaco (SK)": "SK",
    "Esloveno (SL)": "SL",
    "Sueco (SV)": "SV",
    "Turco (TR)": "TR",
    "Ucraniano (UK)": "UK",
    "Chino (ZH)": "ZH"
}

# Reorganizar los idiomas para que los primeros tres sean Inglés, Español y Portugués
priority = ["Inglés (EN)", "Español (ES)", "Portugués (PT-BR)"]
others = [lang for lang in idiomas.keys() if lang not in priority]
others.sort()  # Ordena alfabéticamente los demás idiomas
ordered_options = priority + others

# Distribución en dos columnas iguales para entrada y salida
col1, col2 = st.columns(2)

with col1:
    st.markdown("<div class='panel-title'>Entrada</div>", unsafe_allow_html=True)
    st.markdown("<div class='small-text'>Idioma: Auto-detectado</div>", unsafe_allow_html=True)
    # Área de texto para ingresar el contenido a traducir
    input_text = st.text_area("", height=300, placeholder="Introduce el texto a traducir...")

with col2:
    st.markdown("<div class='panel-title'>Traducción</div>", unsafe_allow_html=True)
    # Selección del idioma de destino usando la lista ordenada
    target_language = st.selectbox("Selecciona el idioma de destino", options=ordered_options)
    # Contenedor para mostrar la traducción (se actualizará luego)
    output_placeholder = st.empty()

# Botón de traducción (centrado debajo de las columnas)
translate_clicked = st.button("Traducir")

if translate_clicked:
    if not input_text.strip():
        st.error("Por favor, introduce un texto válido para traducir.")
    else:
        # Configuración de la API de DeepL (usa el endpoint gratuito si es el plan Free)
        DEEPL_API_KEY = "2ebe1f84-15df-422e-9239-d802082f310c:fx"  # Reemplaza con tu clave API real
        DEEPL_ENDPOINT = "https://api-free.deepl.com/v2/translate"
        
        # Preparar los datos para la solicitud
        data = {
            "auth_key": DEEPL_API_KEY,
            "text": input_text,
            "target_lang": idiomas[target_language]
        }
        
        response = requests.post(DEEPL_ENDPOINT, data=data)
        
        if response.status_code == 200:
            result = response.json()
            translated_text = result.get("translations", [])[0].get("text", "")
            # Mostrar la traducción con el estilo definido
            output_html = f"<div class='output-box'>{translated_text}</div>"
            output_placeholder.markdown(output_html, unsafe_allow_html=True)
        else:
            st.error(f"Error en la solicitud: {response.status_code} - {response.text}")
