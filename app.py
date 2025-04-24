import streamlit as st
from backend.ocr import perform_ocr, find_total
from frontend.display import show_uploaded_image
from PIL import Image

# --- Page config ---
st.set_page_config(
    page_title="🧾 OCR Tickets Français",
    page_icon="🧾",
    layout="wide",
)

# --- Dark background & white text CSS ---
st.markdown(
    """
    <style>
    .stApp { background-color: #000; }
    .stApp, .css-1v0mbdj, .css-1d391kg, .css-1r6slb0 { color: #fff; }
    .stButton>button, .stMetric { background-color: #222 !important; color: #fff !important; }
    .stCodeBlock pre { background-color: #111 !important; color: #fff !important; }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- Sidebar ---
with st.sidebar:
    st.title("OCR Tickets")
    st.write(
        """
        • Téléchargez un ticket/facture  
        • Obtenez son texte et son total  
        • Mode dark  
        """
    )
    st.markdown("---")
    st.write("Made with ❤️ & [docTR](https://github.com/mindee/doctr)")

# --- Main title ---
st.markdown("<h1 style='color:white'>🧾 OCR Tickets Français</h1>", unsafe_allow_html=True)

# --- File uploader ---
uploaded = st.file_uploader("Choisissez une image (PNG/JPG/JPEG)", type=["png","jpg","jpeg"])

if uploaded:
    # Read PIL image
    img = Image.open(uploaded)

    # Create a placeholder for the image
    img_placeholder = st.empty()
    img_placeholder.image(img, caption="Image originale", use_column_width=True)

    # Extraction button
    if st.button("🚀 Extraire le texte"):
        # Remove the image
        img_placeholder.empty()

        with st.spinner("Analyse en cours…"):
            text = perform_ocr(img)

        if text.startswith("Erreur"):
            st.error(text)
        else:
            # Layout: text on left, total on right
            col_text, col_total = st.columns([3, 1])
            with col_text:
                st.subheader("📄 Texte extrait")
                st.code(text, language="text")
            with col_total:
                st.subheader("💰 Total détecté")
                total = find_total(text)
                if total == "Non détecté":
                    st.warning("Aucun total trouvé")
                else:
                    st.metric(label="Montant (€)", value=f"{total} €")
