"""Pestaña 2: analizar varias frases a la vez y descargar los resultados."""

import pandas as pd
import streamlit as st

from detector.config import MAX_FRASES_LOTE
from detector.graficos import grafico_conteo_emociones
from detector.modelo import clasificar, emocion_principal
from detector.utilidades import a_csv, con_emoji, frases_desde_csv, frases_desde_texto

OPCION_ESCRIBIR = "Escribirlas (una por línea)"
OPCION_CSV = "Subir un archivo CSV"


def _pedir_frases() -> list[str]:
    """Muestra la entrada elegida (texto o CSV) y devuelve la lista de frases."""
    origen = st.radio("¿De dónde salen las frases?", [OPCION_ESCRIBIR, OPCION_CSV], horizontal=True)

    if origen == OPCION_ESCRIBIR:
        texto = st.text_area("Frases (una por línea)", height=180,
                             placeholder="I am so happy\nI am scared of the dark\n...")
        return frases_desde_texto(texto)

    archivo = st.file_uploader("Archivo CSV", type="csv",
                               help="Se usa la columna 'frase', 'texto' o 'text'; si no existe, la primera columna.")
    if archivo is None:
        return []
    try:
        frases, columna = frases_desde_csv(archivo)
    except Exception as error:
        st.error(f"❌ No se pudo leer el CSV: {error}")
        return []
    if not columna:
        st.warning("⚠️ El CSV está vacío.")
        return []
    st.caption(f"Columna usada: **{columna}** · {len(frases)} frases encontradas")
    return frases


def _analizar(clasificador, frases: list[str]) -> pd.DataFrame:
    """Clasifica las frases y arma la tabla de resultados (sin depender del umbral)."""
    with st.spinner(f"Analizando {len(frases)} frases..."):
        resultados = clasificar(clasificador, frases)

    filas = []
    for frase, probs in zip(frases, resultados):
        emocion, confianza = emocion_principal(probs)
        filas.append({"frase": frase, "emoción_base": emocion, "confianza": confianza})
    return pd.DataFrame(filas)


def _tabla_para_mostrar(df: pd.DataFrame, umbral: float) -> pd.DataFrame:
    """Da formato a la tabla. El aviso de confianza baja se recalcula si cambia el umbral."""
    return pd.DataFrame({
        "frase": df["frase"],
        "emoción": df["emoción_base"].map(con_emoji),
        "confianza (%)": (df["confianza"] * 100).round(1),
        "confianza baja": df["confianza"].map(lambda c: "⚠️ sí" if c < umbral else "no"),
    })


def _mostrar_resultados(umbral: float) -> None:
    df = st.session_state.resultados_lote
    if df is None or df.empty:
        return

    tabla = _tabla_para_mostrar(df, umbral)
    st.dataframe(tabla, width="stretch", hide_index=True)
    st.altair_chart(grafico_conteo_emociones(df), width="stretch")
    st.download_button("⬇️ Descargar resultados (CSV)", a_csv(tabla),
                       file_name="resultados_emociones.csv", mime="text/csv",
                       on_click="ignore")   # descargar no borra los resultados de pantalla


def mostrar(clasificador, umbral: float) -> None:
    st.write("Analiza varias frases a la vez y descarga los resultados en CSV.")
    frases = _pedir_frases()

    if st.button("🔍 Analizar frases", type="primary", key="analizar_lote"):
        if not frases:
            st.warning("⚠️ No hay frases para analizar.")
            st.session_state.resultados_lote = None
        else:
            if len(frases) > MAX_FRASES_LOTE:
                st.warning(f"Se analizarán solo las primeras {MAX_FRASES_LOTE} frases.")
                frases = frases[:MAX_FRASES_LOTE]
            st.session_state.resultados_lote = _analizar(clasificador, frases)

    _mostrar_resultados(umbral)
