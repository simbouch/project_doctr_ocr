import streamlit as st
from PIL import Image

def show_uploaded_image(uploaded_file, caption="Image"):
    """
    Affiche l'image téléchargée via Streamlit et retourne l'objet PIL.
    """
    try:
        img = Image.open(uploaded_file)
        st.image(img, caption=caption, use_column_width=True)
        return img
    except Exception as e:
        st.error(f"Impossible de lire l’image : {e}")
        return None
