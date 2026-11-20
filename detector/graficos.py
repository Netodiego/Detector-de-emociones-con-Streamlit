"""Gráficos de la app (Altair)."""

import altair as alt
import pandas as pd

from detector.config import COLOR_DESCONOCIDO, COLORES


def grafico_probabilidades(probs: dict[str, float]) -> alt.LayerChart:
    """Barras horizontales ordenadas de mayor a menor, con el porcentaje de cada emoción."""
    df = pd.DataFrame({"emoción": list(probs.keys()), "probabilidad": list(probs.values())})
    df = df.sort_values("probabilidad", ascending=False)
    df["porcentaje"] = (df["probabilidad"] * 100).map("{:.1f} %".format)
    orden = list(df["emoción"])

    colores = alt.Scale(
        domain=orden,
        range=[COLORES.get(e, COLOR_DESCONOCIDO) for e in orden],
    )
    barras = alt.Chart(df).mark_bar(cornerRadiusEnd=4).encode(
        x=alt.X("probabilidad:Q", title="Probabilidad",
                scale=alt.Scale(domain=[0, 1.12]),   # espacio extra para la etiqueta
                axis=alt.Axis(format="%", values=[0, 0.25, 0.5, 0.75, 1])),
        y=alt.Y("emoción:N", sort=orden, title=None),
        color=alt.Color("emoción:N", scale=colores, legend=None),
        tooltip=["emoción", "porcentaje"],
    )
    etiquetas = barras.mark_text(align="left", dx=5, fontWeight="bold").encode(text="porcentaje:N")
    return (barras + etiquetas).properties(height=260)


def grafico_conteo_emociones(df: pd.DataFrame, columna: str = "emoción_base") -> alt.Chart:
    """Cuántas frases cayeron en cada emoción (pestaña de varias frases), con los mismos colores."""
    conteo = df[columna].value_counts().rename_axis("emoción").reset_index(name="frases")
    orden = list(conteo["emoción"])
    colores = alt.Scale(
        domain=orden,
        range=[COLORES.get(e, COLOR_DESCONOCIDO) for e in orden],
    )
    return alt.Chart(conteo).mark_bar(cornerRadiusEnd=4).encode(
        x=alt.X("frases:Q", title="Número de frases", axis=alt.Axis(tickMinStep=1)),
        y=alt.Y("emoción:N", sort=orden, title=None),
        color=alt.Color("emoción:N", scale=colores, legend=None),
        tooltip=["emoción", "frases"],
    ).properties(height=max(120, 40 * len(conteo)))
