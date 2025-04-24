import re
import numpy as np
from PIL import Image
from doctr.models import ocr_predictor

# Initialise la pipeline OCR de docTR
pipeline = ocr_predictor(pretrained=True)

def perform_ocr(image: Image.Image) -> str:
    """
    Effectue l'OCR sur une image PIL et retourne le texte brut organisé par blocs.
    """
    try:
        arr = np.array(image)
        document = pipeline([arr])
        extracted = ""
        for page in document.pages:
            for block in page.blocks:
                for line in block.lines:
                    line_text = " ".join(w.value for w in line.words)
                    extracted += line_text + "\n"
                extracted += "\n"
        return extracted.strip()
    except Exception as e:
        return f"Erreur lors de l'OCR : {e}"

def find_total(text: str) -> str:
    """
    Détecte le montant total sur un ticket/facture français.
    1) Cherche explicitement 'Total TTC', 'Total HT', 'Total à payer', 'Montant total', ou un montant suivi de '€'
    2) À défaut, renvoie le plus grand montant trouvé sur le ticket.
    """
    flat = text.replace("\n", " ")

    def normalize_amt(s: str) -> float:
        """Transforme '1 234,56' en 1234.56"""
        return float(s.replace(" ", "").replace(",", "."))

    patterns = [
        r"(?i)total\s*(?:à payer)?\s*(?:ttc)?\s*[:–-]?\s*€?\s*([0-9 ]+[,.]\d{2})",
        r"(?i)total\s*ht\s*[:–-]?\s*€?\s*([0-9 ]+[,.]\d{2})",
        r"(?i)montant\s*total\s*[:–-]?\s*€?\s*([0-9 ]+[,.]\d{2})",
        r"([0-9 ]+[,.]\d{2})\s*€",
    ]
    for pat in patterns:
        m = re.search(pat, flat)
        if m:
            return f"{normalize_amt(m.group(1)):.2f}"

    # Fallback: extraire tous les montants et prendre le plus élevé
    all_amts = re.findall(r"([0-9 ]+[,.]\d{2})", flat)
    if all_amts:
        nums = [normalize_amt(a) for a in all_amts]
        return f"{max(nums):.2f}"

    return "Non détecté"
