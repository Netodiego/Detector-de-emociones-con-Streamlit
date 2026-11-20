"""Pestaña 3: historial de frases analizadas en la sesión."""

import pandas as pd
import streamlit as st

from detector import estado
from detector.utilidades import a_csv


def mostrar() -> None:
    historial = st.session_state.historial
    if not historial:
        st.info("Todavía no has analizado ninguna frase en esta sesión.")
        return

    df = pd.DataFrame(historial[::-1])   # lo más reciente arriba
    st.write(f"Frases analizadas en esta sesión: **{len(df)}**")
    st.dataframe(df, width="stretch", hide_index=True)

    col1, col2 = st.columns(2)
    col1.download_button("⬇️ Descargar historial (CSV)", a_csv(df),
                         file_name="historial_emociones.csv", mime="text/csv",
                         on_click="ignore")
    col2.button("🗑️ Borrar historial", on_click=estado.borrar_historial)
