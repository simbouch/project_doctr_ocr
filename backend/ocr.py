import numpy as np
from PIL import Image
from doctr.models import ocr_predictor

# Initialisation de la pipeline OCR de docTR avec le modèle pré-entraîné
pipeline = ocr_predictor(pretrained=True)

def perform_ocr(image: Image.Image) -> str:
    """
    Effectue l'OCR sur une image PIL en utilisant docTR et organise le texte extrait.

    Paramètres :
        image (PIL.Image.Image): L'image à traiter.

    Retourne :
        str: Le texte extrait de l'image, organisé par blocs avec séparation claire.
    """
    try:
        # Convertir l'image PIL en tableau numpy
        image_array = np.array(image)
        
        # Appeler la pipeline et obtenir un objet Document
        document = pipeline([image_array])
        
        # Concaténer le texte extrait avec séparation des blocs
        extracted_text = ""
        for page in document.pages:
            for block in page.blocks:
                block_text = ""
                for line in block.lines:
                    # Joindre les mots d'une ligne avec un espace
                    line_text = " ".join(word.value for word in line.words)
                    block_text += line_text + "\n"
                # Ajouter le texte du bloc suivi d'une ligne vide pour séparation
                extracted_text += block_text + "\n"
        return extracted_text.strip()  # Supprimer les espaces ou lignes vides en excès
    except Exception as e:
        return f"Erreur lors de l'OCR : {str(e)}"