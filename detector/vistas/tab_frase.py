"""Pestaña 1: analizar una sola frase."""

import streamlit as st

from detector import estado
from detector.config import COLUMNAS_EJEMPLOS, FRASES_EJEMPLO, LARGO_MAX_BOTON
from detector.graficos import grafico_probabilidades
from detector.modelo import clasificar, emocion_principal
from detector.utilidades import acortar, con_emoji


def _botones_ejemplo() -> None:
    st.caption("¿No se te ocurre nada? Prueba con una frase de ejemplo:")
    columnas = st.columns(COLUMNAS_EJEMPLOS)
    for i, frase in enumerate(FRASES_EJEMPLO):
        columnas[i % COLUMNAS_EJEMPLOS].button(
            acortar(frase, LARGO_MAX_BOTON),
            key=f"ejemplo_{i}", help=frase,
            on_click=estado.usar_ejemplo, args=(frase,), width="stretch",
        )


def _analizar(clasificador) -> None:
    frase = st.session_state.texto.strip()
    if not frase:
        st.warning("⚠️ Escribe una frase antes de analizar.")
        estado.limpiar_ultimo()
        return

    probs = clasificar(clasificador, [frase])[0]
    emocion, confianza = emocion_principal(probs)
    estado.guardar_ultimo(frase, probs)
    estado.agregar_al_historial(frase, emocion, confianza)


def _mostrar_resultado(umbral: float) -> None:
    """Muestra el último resultado (se mantiene aunque se mueva el umbral)."""
    ultimo = st.session_state.ultimo
    if not ultimo:
        return

    probs = ultimo["probs"]
    emocion, confianza = emocion_principal(probs)

    st.subheader("Resultado")
    col1, col2 = st.columns(2)
    col1.metric("Emoción detectada", con_emoji(emocion))
    col2.metric("Confianza", f"{confianza * 100:.1f} %")

    if confianza < umbral:
        st.warning(f"🤔 Confianza baja: la emoción principal no supera el umbral de "
                   f"{umbral * 100:.0f} %. Revisa la frase o tómalo con cautela.")

    st.altair_chart(grafico_probabilidades(probs), width="stretch")
    st.caption(f"Frase analizada: “{ultimo['frase']}”")


def mostrar(clasificador, umbral: float) -> None:
    _botones_ejemplo()

    st.text_area("Frase a analizar", key="texto", height=100,
                 placeholder="Ej.: I can't wait to see you again!")

    if st.button("🔍 Analizar emoción", type="primary"):
        _analizar(clasificador)

    _mostrar_resultado(umbral)
