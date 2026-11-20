"""
Detector de emociones con Streamlit
Usa el modelo DistilBERT ajustado en clase (Bloque 4.4 del notebook).

Ejecutar con:  streamlit run app.py

Este archivo solo arma la página: la lógica vive en el paquete `detector/`.
"""

import streamlit as st

from detector.config import TITULO_PAGINA, ICONO_PAGINA
from detector.estado import inicializar_estado
from detector.vistas import encabezado, barra_lateral, tab_frase, tab_lote, tab_historial


def main():
    st.set_page_config(page_title=TITULO_PAGINA, page_icon=ICONO_PAGINA, layout="centered")
    inicializar_estado()

    encabezado.mostrar()
    clasificador = encabezado.obtener_clasificador()   # detiene la app si no hay modelo
    umbral = barra_lateral.mostrar()

    pestana_frase, pestana_lote, pestana_historial = st.tabs(
        ["📝 Una frase", "📋 Varias frases", "🕘 Historial"]
    )
    with pestana_frase:
        tab_frase.mostrar(clasificador, umbral)
    with pestana_lote:
        tab_lote.mostrar(clasificador, umbral)
    with pestana_historial:
        tab_historial.mostrar()


if __name__ == "__main__":
    main()
