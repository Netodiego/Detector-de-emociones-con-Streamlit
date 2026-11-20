"""Funciones auxiliares: formato de etiquetas, lectura de frases y exportación a CSV."""

import pandas as pd

from detector.config import COLUMNAS_CSV, EMOJI_DESCONOCIDO, EMOJIS


def con_emoji(emocion: str) -> str:
    return f"{EMOJIS.get(emocion, EMOJI_DESCONOCIDO)} {emocion}"


def acortar(texto: str, largo_max: int) -> str:
    """Recorta un texto largo y le agrega puntos suspensivos."""
    return texto if len(texto) <= largo_max else texto[: largo_max - 2] + "…"


def frases_desde_texto(texto: str) -> list[str]:
    """Una frase por línea, sin líneas vacías."""
    return [linea.strip() for linea in texto.splitlines() if linea.strip()]


def frases_desde_csv(archivo) -> tuple[list[str], str]:
    """
    Lee un CSV y devuelve (frases, columna_usada).
    Usa la columna 'frase', 'texto' o 'text'; si no existe, la primera columna.
    """
    df = pd.read_csv(archivo)
    if df.empty or len(df.columns) == 0:
        return [], ""
    columna = next((c for c in COLUMNAS_CSV if c in df.columns), df.columns[0])
    frases = [str(f).strip() for f in df[columna].dropna() if str(f).strip()]
    return frases, columna


def a_csv(df: pd.DataFrame) -> bytes:
    # utf-8-sig para que Excel muestre bien las tildes
    return df.to_csv(index=False).encode("utf-8-sig")
