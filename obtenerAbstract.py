# archivo: extractor_impi_app.py
import streamlit as st
import re
import pandas as pd
import PyPDF2
import requests
from bs4 import BeautifulSoup

url_Espacenet = "https://worldwide.espacenet.com"
url_google_patents = "https://patents.google.com"
url_chatGPT = "https://chatgpt.com/"
st.set_page_config(page_title="Abstract de una patente", layout="centered")
st.title("📄 Obtener el abstract de una patente")
def obtener_abstract_google_patents(patente_id):
    url = f"https://patents.google.com/patent/{patente_id}/en"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        #print("No se pudo acceder a la página")
        return "None"

    soup = BeautifulSoup(response.text, "html.parser")
    
    abstract_tag = soup.find("div", {"class": "abstract"})

    if abstract_tag:
        return abstract_tag.text.strip()
    else:
        print("No se encontró el abstract.")
        return "None"
    
def obtener_abstract_espacenet(patente_id):
    url = f"https://worldwide.espacenet.com/patent/search?q={patente_id}"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    print(url)
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return "None"

    soup = BeautifulSoup(response.text, "html.parser")
    
    abstract_tag = soup.find("div", {"class": "abstract"})

    if abstract_tag:
        return abstract_tag.text.strip()
    else:
        return "None"

# Subida de archivo
numero_patente = st.text_input("Ingresa el número de patente:", placeholder="Ej: ABC123")

# Botón de búsqueda
if st.button("Buscar"):
    if numero_patente:  # Si se ingresó texto
        abstract = obtener_abstract_google_patents(numero_patente)
        if abstract == "None":
            abstract = obtener_abstract_espacenet(numero_patente)
            if abstract == "None":
                #if st.button("Abrir Espacenet"):
                 #   js = f"window.open('{url_Espacenet}')"
                  #  st.components.v1.html(f"<script>{js}</script>", height=0)
                st.markdown(f"""
                    <a href="{url_Espacenet}" target="_blank">
                        <button style="color: white; background-color: #FF4B4B; border: none; padding: 0.5rem 1rem; border-radius: 0.25rem;">
                            Abrir Espacenet
                        </button>
                    </a>
                    """, unsafe_allow_html=True)
                st.markdown(f"""
                    <a href="{url_google_patents}" target="_blank">
                        <button style="color: white; background-color: #FF4B4B; border: none; padding: 0.5rem 1rem; border-radius: 0.25rem;">
                            Abrir Google Patents
                        </button>
                    </a>
                    """, unsafe_allow_html=True)
                st.markdown(f"""
                    <a href="{url_chatGPT}" target="_blank">
                        <button style="color: white; background-color: #FF4B4B; border: none; padding: 0.5rem 1rem; border-radius: 0.25rem;">
                            Abrir ChatGPT
                        </button>
                    </a>
                    """, unsafe_allow_html=True)
        st.success(abstract)

    else:
        # Mensaje de error si no se ingresó nada
        st.warning("⚠️ Por favor, ingresa un número de patente.")

# Espacio en blanco para mejor formato
st.write("")  # Separador visual