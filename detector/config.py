"""
Configuración general de la aplicación.
Todo lo que se quiera ajustar (ruta del modelo, idioma, límites, colores) se cambia aquí.
"""

import os
from pathlib import Path

# ------------------------------------------------------------------
# Rutas
# ------------------------------------------------------------------
CARPETA_PROYECTO = Path(__file__).resolve().parent.parent

# Carpeta generada con trainer.save_model(). Se puede cambiar con la variable de entorno RUTA_MODELO.
RUTA_MODELO = Path(os.getenv("RUTA_MODELO", CARPETA_PROYECTO / "modelo_emociones_distilbert"))

# ------------------------------------------------------------------
# Página
# ------------------------------------------------------------------
TITULO_PAGINA = "Detector de emociones"
ICONO_PAGINA = "🎭"

# ------------------------------------------------------------------
# Modelo
# ------------------------------------------------------------------
IDIOMA_MODELO = "inglés"      # cambiar a "español" si usan un modelo en español
MODELO_BASE = "distilbert-base-uncased"
DATASET = "dair-ai/emotion"
MAX_TOKENS = 128              # las frases más largas se truncan
MAX_FRASES_LOTE = 500         # límite para el análisis por lotes

# ------------------------------------------------------------------
# Umbral de confianza (slider de la barra lateral)
# ------------------------------------------------------------------
UMBRAL_POR_DEFECTO = 0.50
UMBRAL_PASO = 0.05

# ------------------------------------------------------------------
# Emociones: emoji, color y traducción (los nombres son los id2label del notebook)
# ------------------------------------------------------------------
EMOJIS = {
    "tristeza": "😢", "alegría": "😄", "amor": "❤️",
    "ira": "😠", "miedo": "😨", "sorpresa": "😲",
}
COLORES = {
    "tristeza": "#4C72B0", "alegría": "#F2B701", "amor": "#E15F99",
    "ira": "#C44E52", "miedo": "#8172B3", "sorpresa": "#55A868",
}
COLOR_DESCONOCIDO = "#999999"
EMOJI_DESCONOCIDO = "🔹"

# Por si el modelo se guardó con las etiquetas en inglés
TRADUCCION = {
    "sadness": "tristeza", "joy": "alegría", "love": "amor",
    "anger": "ira", "fear": "miedo", "surprise": "sorpresa",
}

# ------------------------------------------------------------------
# Frases de ejemplo de la pestaña "Una frase"
# ------------------------------------------------------------------
FRASES_EJEMPLO = [
    "I feel so happy and grateful today",
    "I am terrified of what might happen tomorrow",
    "I miss my grandmother so much, I can't stop crying",
    "I am furious, they lied to me again",
    "I love spending time with you",
    "I can't believe it, I won the lottery!",
    "Oh great, another Monday. I'm just thrilled",   # sarcasmo
    "I am not sad at all",                           # negación
]
COLUMNAS_EJEMPLOS = 4
LARGO_MAX_BOTON = 28

# Columnas que se buscan (en este orden) al subir un CSV
COLUMNAS_CSV = ["frase", "texto", "text"]
