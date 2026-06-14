"""
Smart-Guard Support Center - Agente 1: Atención al Cliente
Responsabilidad: Interpretar el mensaje del cliente, detectar intención,
categoría del problema, componente afectado y urgencia inicial.
"""

import re


# Mapa de intenciones con sus palabras clave asociadas
INTENT_KEYWORDS = {
    "problema_rfid": [
        "rfid", "no detecta", "lector", "etiqueta", "tag", "tags",
        "lectura", "no lee", "escaneo", "identifica", "identificar",
        "producto no detectado", "no reconoce",
    ],
    "problema_bateria": [
        "batería", "bateria", "baja", "sin carga", "se apaga", "energía",
        "descargado", "dock", "cargando", "no carga", "cargador",
    ],
    "problema_pago": [
        "pago", "no paga", "no valida", "finalizar compra", "cobro",
        "transacción", "nfc", "qr", "no permite pagar", "error de pago",
        "no finaliza", "finalizar",
    ],
    "problema_pantalla": [
        "pantalla", "display", "no responde", "congelada", "negra",
        "táctil", "tactil", "no enciende", "pantalla muerta", "no toca",
    ],
    "problema_sesion": [
        "sesión", "sesion", "iniciar sesión", "login", "no inicia",
        "no permite acceder", "acceso", "usuario", "no ingresa",
    ],
    "problema_inventario": [
        "total", "no coincide", "productos físicos", "diferencia",
        "no existe", "no registrado", "inventario", "base de datos",
        "producto no encontrado", "no vinculado",
    ],
    "consulta_estado": [
        "estado", "cómo está", "como esta", "consulta", "información",
        "info", "status",
    ],
    "solicitud_mantenimiento": [
        "mantenimiento", "revisión", "revision", "reparar", "reparación",
        "servicio", "técnico", "enviar técnico",
    ],
    "reporte_falla": [
        "falla", "error", "problema", "no funciona", "roto", "defecto",
        "avería", "averia", "raspberry", "no responde el sistema",
    ],
}

# Palabras clave de urgencia
URGENCY_HIGH_KEYWORDS = [
    "urgente", "inmediato", "ahora", "crítico", "critico",
    "no funciona nada", "varios carritos", "tres carritos",
    "todos los carritos", "raspberry no responde",
]
URGENCY_LOW_KEYWORDS = [
    "lento", "a veces", "ocasional", "poco", "menor",
]

# Mapa de componentes por intención
COMPONENT_MAP = {
    "problema_rfid":      "Lector RFID",
    "problema_bateria":   "Módulo de batería",
    "problema_pago":      "Sistema de pago",
    "problema_pantalla":  "Pantalla táctil",
    "problema_sesion":    "Pantalla táctil",
    "problema_inventario":"Base de datos local",
    "reporte_falla":      "Raspberry Pi 4",
    "consulta_estado":    "General",
    "solicitud_mantenimiento": "Hardware general",
    "desconocida":        "Desconocido",
}

# Mapa de categorías por intención
CATEGORY_MAP = {
    "problema_rfid":      "Identificación de productos",
    "problema_bateria":   "Energía y carga",
    "problema_pago":      "Sistema de pago",
    "problema_pantalla":  "Pantalla e interfaz",
    "problema_sesion":    "Gestión de sesión",
    "problema_inventario":"Inventario y base de datos",
    "reporte_falla":      "Falla de sistema",
    "consulta_estado":    "Consulta general",
    "solicitud_mantenimiento": "Mantenimiento preventivo",
    "desconocida":        "Sin categoría",
}


def _normalize(text: str) -> str:
    """Normaliza el texto a minúsculas sin caracteres especiales."""
    text = text.lower()
    replacements = {"á": "a", "é": "e", "í": "i", "ó": "o", "ú": "u", "ñ": "n"}
    for k, v in replacements.items():
        text = text.replace(k, v)
    return text


def _detect_cart_id(text: str) -> str | None:
    """Extrae el ID del carrito del texto (ej. SGC-004)."""
    match = re.search(r'\bSGC-\d{3}\b', text.upper())
    return match.group(0) if match else None


def _detect_intent(normalized: str) -> str:
    """Detecta la intención principal del mensaje."""
    scores = {}
    for intent, keywords in INTENT_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in normalized)
        if score > 0:
            scores[intent] = score

    if not scores:
        return "desconocida"

    # Intención con mayor puntaje
    return max(scores, key=scores.get)


def _detect_urgency(normalized: str, intent: str) -> str:
    """Determina la urgencia inicial del reporte."""
    if any(kw in normalized for kw in URGENCY_HIGH_KEYWORDS):
        return "alta"
    if intent in ("problema_pago", "reporte_falla"):
        return "alta"
    if any(kw in normalized for kw in URGENCY_LOW_KEYWORDS):
        return "baja"
    return "media"


def _extract_keywords(normalized: str, intent: str) -> list:
    """Extrae las palabras clave detectadas del mensaje."""
    found = []
    all_kws = INTENT_KEYWORDS.get(intent, [])
    for kw in all_kws:
        if kw in normalized:
            found.append(kw)
    return found[:5]  # Máximo 5 palabras clave


def process(message: str, client_id: int = None) -> dict:
    """
    Agente 1 — Procesa el mensaje del cliente y retorna un análisis estructurado.

    Args:
        message: Texto libre del reporte del cliente.
        client_id: ID del cliente (opcional).

    Returns:
        dict con intent, category, component, cart_id, urgency, keywords, raw_message.
    """
    normalized = _normalize(message)

    intent   = _detect_intent(normalized)
    cart_id  = _detect_cart_id(message)
    urgency  = _detect_urgency(normalized, intent)
    keywords = _extract_keywords(normalized, intent)
    category  = CATEGORY_MAP.get(intent, "Sin categoría")
    component = COMPONENT_MAP.get(intent, "Desconocido")

    result = {
        "intent":      intent,
        "category":    category,
        "component":   component,
        "cart_id":     cart_id,
        "urgency":     urgency,
        "keywords":    keywords,
        "client_id":   client_id,
        "raw_message": message,
        "agent":       "Agente 1 — Atención al Cliente",
        "status":      "ok",
        "notes": (
            f"Se detectó la intención '{intent}' con {len(keywords)} palabra(s) clave. "
            f"Componente probable: {component}. Urgencia inicial: {urgency}."
        ),
    }

    return result


# --- Prueba directa ---
if __name__ == "__main__":
    tests = [
        "El carrito SGC-004 no detecta productos RFID.",
        "El carrito SGC-002 tiene batería baja aunque está en la bahía.",
        "El carrito SGC-007 no permite finalizar la compra.",
        "El total del carrito no coincide con los productos físicos.",
        "La pantalla del carrito SGC-003 no responde.",
    ]
    for t in tests:
        result = process(t)
        print(f"\n[Test]: {t}")
        for k, v in result.items():
            print(f"  {k}: {v}")
