"""
Smart-Guard Support Center - Motor de Inferencia
Aplica reglas IF/THEN sobre los hechos detectados por el Agente 1.
Soporta inferencia encadenada simple.
"""

from base.base_conocimiento import get_all_rules

# Jerarquía de prioridades para comparar
PRIORITY_ORDER = {"critica": 4, "alta": 3, "media": 2, "baja": 1}


def _text_matches_conditions(text: str, conditions: list) -> int:
    """
    Cuenta cuántas condiciones de una regla están presentes en el texto.
    Retorna el número de condiciones satisfechas.
    """
    text_lower = text.lower()
    return sum(1 for cond in conditions if cond.lower() in text_lower)


def _intent_matches(intent: str, rule_intents: list) -> bool:
    """Verifica si la intención detectada coincide con las intenciones de la regla."""
    if not rule_intents:
        return False
    return intent in rule_intents


def run(agent1_output: dict, previous_tickets_count: int = 0) -> dict:
    """
    Motor de inferencia principal.

    Args:
        agent1_output: Resultado del Agente 1 (dict).
        previous_tickets_count: Número de tickets previos del mismo carrito.

    Returns:
        dict con reglas aplicadas, prioridad final, diagnóstico, recomendación,
        explicación y datos para logs.
    """
    rules = get_all_rules()
    raw_message = agent1_output.get("raw_message", "")
    intent = agent1_output.get("intent", "desconocida")
    urgency = agent1_output.get("urgency", "media")

    matched_rules = []
    all_explanations = []

    # --- PASO 1: Evaluar todas las reglas ---
    for rule in rules:
        text_score = _text_matches_conditions(raw_message, rule["conditions"])
        intent_match = _intent_matches(intent, rule.get("intent_match", []))

        # Una regla aplica si hay coincidencia de intención O ≥2 condiciones en texto
        if intent_match or text_score >= 2:
            confidence = min(1.0, (text_score * 0.15) + (0.5 if intent_match else 0.0))
            matched_rules.append({
                "rule": rule,
                "confidence": round(confidence, 2),
                "text_score": text_score,
                "intent_match": intent_match,
            })

    # --- PASO 2: Ordenar por prioridad y confianza ---
    matched_rules.sort(
        key=lambda x: (
            PRIORITY_ORDER.get(x["rule"]["priority"], 0),
            x["confidence"],
        ),
        reverse=True,
    )

    # --- PASO 3: Seleccionar regla principal ---
    if matched_rules:
        best = matched_rules[0]
        primary_rule = best["rule"]
    else:
        # Regla por defecto si no hay coincidencias
        primary_rule = {
            "id": "R0",
            "name": "Regla por defecto",
            "result": "Falla general no clasificada",
            "priority": urgency,
            "component": agent1_output.get("component", "Desconocido"),
            "recommendation": (
                "No se encontró una regla específica. Se recomienda revisión técnica manual."
            ),
            "explanation": (
                "El mensaje no coincidió con ninguna regla predefinida. "
                "Se aplicó la clasificación por urgencia detectada."
            ),
        }
        matched_rules = [{"rule": primary_rule, "confidence": 0.3}]

    # --- PASO 4: Escalamiento por historial (Regla R8) ---
    priority = primary_rule["priority"]
    chaining_applied = False

    if previous_tickets_count >= 2:
        chaining_applied = True
        # Escalar prioridad un nivel
        if priority == "baja":
            priority = "media"
        elif priority == "media":
            priority = "alta"
        elif priority == "alta":
            priority = "critica"
        all_explanations.append(
            f" Escalamiento por reincidencia: se detectaron {previous_tickets_count} "
            f"tickets previos en este carrito. Se aplicó la regla R8 de escalamiento."
        )

    # --- PASO 5: Construir explicación acumulada ---
    for item in matched_rules[:3]:  # Máximo 3 reglas en la explicación
        r = item["rule"]
        all_explanations.append(
            f"[{r['id']}] {r['name']} — Confianza: {item['confidence']:.0%}. {r['explanation']}"
        )

    # --- PASO 6: Inferencia encadenada simple ---
    # Si hay problema de batería Y hay falla de pantalla → urgencia más alta
    secondary_intents = [item["rule"]["id"] for item in matched_rules]
    if "R5" in secondary_intents and "R13" in secondary_intents:
        if PRIORITY_ORDER.get(priority, 0) < PRIORITY_ORDER.get("alta", 0):
            priority = "alta"
            all_explanations.append(
                " Inferencia encadenada: se detectaron simultáneamente falla de "
                "batería y pantalla. La prioridad se elevó a Alta."
            )
            chaining_applied = True

    return {
        "primary_rule_id":    primary_rule["id"],
        "primary_rule_name":  primary_rule["name"],
        "diagnosis":          primary_rule["result"],
        "priority":           priority,
        "component":          primary_rule.get("component", agent1_output.get("component")),
        "recommendation":     primary_rule["recommendation"],
        "explanation":        primary_rule["explanation"],
        "all_explanations":   all_explanations,
        "rules_applied":      [item["rule"]["id"] for item in matched_rules],
        "rules_detail":       matched_rules,
        "chaining_applied":   chaining_applied,
        "previous_tickets":   previous_tickets_count,
        "confidence":         matched_rules[0]["confidence"] if matched_rules else 0.3,
    }


if __name__ == "__main__":
    test_input = {
        "intent": "problema_rfid",
        "category": "Identificación de productos",
        "component": "Lector RFID",
        "cart_id": "SGC-004",
        "urgency": "media",
        "keywords": ["no detecta", "rfid"],
        "raw_message": "El carrito SGC-004 no detecta productos RFID.",
    }
    result = run(test_input, previous_tickets_count=0)
    print("\n=== Resultado del Motor de Inferencia ===")
    for k, v in result.items():
        print(f"  {k}: {v}")
