import streamlit as st
import fitz  # PyMuPDF
import re

# --- 1. Base de données simplifiée (Substances interdites) ---
# En production, on lierait ceci à une API ZDHC ou un fichier Excel
MRSL_DATABASE = {
    "71-43-2": "Benzène",
    "68-12-2": "Diméthylformamide (DMFu)",
    "75-09-2": "Chlorure de méthylène"
}

def extract_cas_numbers(text):
    # Regex pour trouver des numéros CAS (ex: 123-45-6)
    cas_pattern = r'\b\d{2,7}-\d{2}-\d\b'
    return set(re.findall(cas_pattern, text))

# --- 2. Interface Utilisateur ---
st.title("🛡️ Analyseur de FDS : Check MRSL/RSL")
st.write("Téléchargez une FDS en PDF pour vérifier la conformité des substances.")

uploaded_file = st.file_uploader("Choisir une FDS (PDF)", type="pdf")

if uploaded_file is not None:
    # Lecture du PDF
    with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
        text = ""
        for page in doc:
            text += page.get_text()
    
    # Extraction des CAS
    found_cas = extract_cas_numbers(text)
    
    st.subheader("Analyse en cours...")
    
    danger_zone = []
    for cas in found_cas:
        if cas in MRSL_DATABASE:
            danger_zone.append(f"⚠️ **{MRSL_DATABASE[cas]}** (CAS: {cas})")
    
    # --- 3. Résultat ---
    if danger_zone:
        st.error("PRODUIT NON CONFORME / ALERTE")
        for item in danger_zone:
            st.write(item)
    else:
        st.success("Aucune substance de la liste MRSL détectée automatiquement.")
        st.info(f"Numéros CAS détectés : {', '.join(found_cas)}")
