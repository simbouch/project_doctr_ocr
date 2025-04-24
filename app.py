import streamlit as st
from backend.ocr import perform_ocr
from frontend.display import show_uploaded_image

def main():
    """Lance l'application OCR avec docTR dans Streamlit."""
    st.title("Application OCR avec docTR")
    
    # Téléchargement de l'image
    uploaded_file = st.file_uploader("Téléchargez une image", type=["png", "jpg", "jpeg"])
    
    if uploaded_file is not None:
        # Afficher l'image et obtenir l'objet PIL
        image = show_uploaded_image(uploaded_file, caption="Image Originale")
        
        if image:
            # Bouton pour lancer l'extraction
            if st.button("Extraire le texte"):
                with st.spinner("Extraction du texte en cours..."):
                    extracted_text = perform_ocr(image)
                
                # Afficher le résultat
                st.subheader("Texte Extrait")
                if extracted_text.startswith("Erreur"):
                    st.error(extracted_text)
                else:
                    # Utiliser markdown pour préserver le formatage
                    st.markdown("```text\n" + extracted_text + "\n```")

if __name__ == "__main__":
    main()