"""
Manejo del estado de la sesión (st.session_state).
Todas las claves que usa la app se definen aquí, en un solo lugar.
"""

from datetime import datetime

import streamlit as st


def _valores_iniciales() -> dict:
    # Función (y no constante) para que cada sesión reciba listas nuevas
    return {
        "texto": "",              # contenido del campo de texto de "Una frase"
        "ultimo": None,           # último resultado de "Una frase": {"frase", "probs"}
        "historial": [],          # frases analizadas en la sesión
        "resultados_lote": None,  # último análisis de "Varias frases" (DataFrame)
    }


def inicializar_estado() -> None:
    for clave, valor in _valores_iniciales().items():
        if clave not in st.session_state:
            st.session_state[clave] = valor


def usar_ejemplo(frase: str) -> None:
    """Callback de los botones de ejemplo: se ejecuta antes de dibujar el campo de texto."""
    st.session_state.texto = frase


def guardar_ultimo(frase: str, probs: dict[str, float]) -> None:
    st.session_state.ultimo = {"frase": frase, "probs": probs}


def limpiar_ultimo() -> None:
    st.session_state.ultimo = None


def agregar_al_historial(frase: str, emocion: str, confianza: float) -> None:
    st.session_state.historial.append({
        "hora": datetime.now().strftime("%H:%M:%S"),
        "frase": frase,
        "emoción": emocion,
        "confianza (%)": round(confianza * 100, 1),
    })


def borrar_historial() -> None:
    st.session_state.historial = []
    st.session_state.ultimo = None
