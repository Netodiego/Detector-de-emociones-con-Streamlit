"""
Carga del modelo y clasificación de frases.
No dibuja nada en pantalla: solo devuelve datos.
"""

from pathlib import Path

import streamlit as st

from detector.config import MAX_TOKENS, TRADUCCION


def modelo_disponible(ruta: Path) -> bool:
    """Indica si la carpeta del modelo existe y tiene su config.json."""
    return (Path(ruta) / "config.json").is_file()


@st.cache_resource(show_spinner="Cargando el modelo, espera un momento...")
def cargar_modelo(ruta: str):
    """Carga el pipeline una sola vez por servidor (gracias a st.cache_resource)."""
    # Se importa aquí para que la app arranque rápido y muestre errores claros si falta la carpeta
    from transformers import pipeline

    # El pipeline lee de la carpeta los pesos, la configuración y el tokenizador
    return pipeline("text-classification", model=ruta, tokenizer=ruta)


def clasificar(clasificador, frases: list[str]) -> list[dict[str, float]]:
    """Recibe una lista de frases y devuelve, por cada una, un diccionario {emoción: probabilidad}."""
    salidas = clasificador(frases, top_k=None, truncation=True, max_length=MAX_TOKENS)
    return [
        {TRADUCCION.get(r["label"], r["label"]): r["score"] for r in salida}
        for salida in salidas
    ]


def emocion_principal(probs: dict[str, float]) -> tuple[str, float]:
    """Devuelve la emoción con mayor probabilidad y esa probabilidad."""
    emocion = max(probs, key=probs.get)
    return emocion, probs[emocion]
