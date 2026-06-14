"""
Smart-Guard Support Center - Configuración Global
"""

import os

# Rutas del proyecto
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
DB_PATH = os.path.join(DATA_DIR, "smartguard_support.db")

# Asegurar que exista el directorio de datos
os.makedirs(DATA_DIR, exist_ok=True)

# Configuración del sistema
APP_NAME = "Smart-Guard Support Center"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "Sistema Experto para Soporte Técnico de Smart-Guard Cart"

# Niveles de prioridad
PRIORITY_LEVELS = {
    "critica": {"label": " Crítica", "color": "#FF4B4B", "order": 1},
    "alta":    {"label": " Alta",    "color": "#FF8C00", "order": 2},
    "media":   {"label": " Media",   "color": "#FFD700", "order": 3},
    "baja":    {"label": " Baja",    "color": "#4CAF50", "order": 4},
}

# Estados de tickets
TICKET_STATES = ["abierto", "en_proceso", "resuelto", "cerrado"]

# Categorías de problemas
PROBLEM_CATEGORIES = [
    "Identificación de productos",
    "Gestión de sesión",
    "Sistema de pago",
    "Energía y carga",
    "Pantalla e interfaz",
    "Red y conectividad",
    "Base de datos local",
    "Hardware general",
    "Incidencia crítica",
]
