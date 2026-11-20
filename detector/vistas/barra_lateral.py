"""Barra lateral: umbral de confianza e información del modelo."""

import streamlit as st

from detector.config import (DATASET, EMOJIS, IDIOMA_MODELO, MODELO_BASE,
                             UMBRAL_PASO, UMBRAL_POR_DEFECTO)
from detector.utilidades import con_emoji


def mostrar() -> float:
    """Dibuja la barra lateral y devuelve el umbral elegido."""
    with st.sidebar:
        st.header("⚙️ Ajustes")
        umbral = st.slider(
            "Umbral de confianza", min_value=0.0, max_value=1.0,
            value=UMBRAL_POR_DEFECTO, step=UMBRAL_PASO,
            help="Si la emoción principal tiene una probabilidad menor a este valor, se muestra una advertencia.",
        )

        st.divider()
        st.header("ℹ️ Sobre el modelo")
        st.markdown(f"""
- **Base:** `{MODELO_BASE}`
- **Ajuste fino:** dataset `{DATASET}`
- **Idioma:** {IDIOMA_MODELO}
- **Clases:** {", ".join(con_emoji(e) for e in EMOJIS)}
""")
    return umbral
