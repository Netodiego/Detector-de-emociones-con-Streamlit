"""Título, aviso de idioma y validación/carga del modelo."""

import streamlit as st

from detector.config import IDIOMA_MODELO, RUTA_MODELO
from detector.modelo import cargar_modelo, modelo_disponible


def mostrar() -> None:
    st.title("🎭 Detector de emociones")
    st.write("Escribe una frase y el modelo te dirá qué emoción expresa: "
             "tristeza, alegría, amor, ira, miedo o sorpresa.")

    if IDIOMA_MODELO == "inglés":
        st.info("🌐 **Idioma del modelo: inglés.** El modelo (DistilBERT) fue preentrenado y ajustado "
                "solo con frases en inglés. Si escribes en español, el resultado no es confiable.")
    else:
        st.info("🌐 **Idioma del modelo: español.** Escribe tus frases en español.")


def obtener_clasificador():
    """Devuelve el clasificador listo para usar. Si algo falla, muestra el error y detiene la app."""
    if not modelo_disponible(RUTA_MODELO):
        st.error(f"❌ No se encontró el modelo en la carpeta **`{RUTA_MODELO.name}`**.\n\n"
                 "Copia junto a `app.py` la carpeta que generaste en el Bloque 4.4 del notebook "
                 "(`trainer.save_model`). Debe contener `config.json`, `model.safetensors` y los "
                 "archivos del tokenizador.")
        st.stop()

    try:
        return cargar_modelo(str(RUTA_MODELO))
    except Exception as error:
        st.error(f"❌ La carpeta `{RUTA_MODELO.name}` existe, pero no se pudo cargar el modelo: {error}")
        st.stop()
