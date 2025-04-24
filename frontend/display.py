import streamlit as st
from PIL import Image

def show_uploaded_image(uploaded_file, caption="Image téléchargée") -> Image.Image:
    """
    Affiche une image téléchargée dans Streamlit et retourne l'objet PIL.

    Paramètres :
        uploaded_file: Fichier téléchargé via Streamlit.
        caption (str): Légende à afficher sous l'image.

    Retourne :
        PIL.Image.Image: L'image ouverte, ou None en cas d'erreur.
    """
    try:
        image = Image.open(uploaded_file)
        st.image(image, caption=caption, use_column_width=True)
        return image
    except Exception as e:
        st.error(f"Erreur lors de l'ouverture de l'image : {e}")
        return None