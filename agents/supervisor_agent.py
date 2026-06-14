"""
Smart-Guard Support Center - Agente 3: Supervisor / Explicador
Responsabilidad: Generar una explicación clara y comprensible del razonamiento
del sistema experto para el usuario final.
"""

PRIORITY_LABELS = {
    "critica": " CRÍTICA",
    "alta":    " ALTA",
    "media":   " MEDIA",
    "baja":    " BAJA",
}

PRIORITY_REASONS = {
    "critica": (
        "La prioridad es CRÍTICA porque la falla compromete gravemente la operación del "
        "supermercado o afecta a múltiples carritos de manera simultánea."
    ),
    "alta": (
        "La prioridad es ALTA porque la falla impide completar transacciones de pago "
        "o afecta funciones esenciales del carrito de manera repetida."
    ),
    "media": (
        "La prioridad es MEDIA porque la falla afecta el funcionamiento normal del "
        "carrito pero no compromete directamente la seguridad ni los pagos."
    ),
    "baja": (
        "La prioridad es BAJA porque la falla es intermitente o tiene impacto "
        "mínimo en la operación del sistema."
    ),
}

INTENT_EXPLANATIONS = {
    "problema_rfid": (
        "El reporte indica una falla en la identificación de productos mediante RFID. "
        "Este es uno de los componentes más críticos del Smart-Guard Cart, ya que "
        "sin él no es posible registrar productos en la lista de compra."
    ),
    "problema_bateria": (
        "El reporte indica un problema con la energía o el sistema de carga del carrito. "
        "Si no se resuelve, el carrito quedará inoperativo cuando la batería se agote."
    ),
    "problema_pago": (
        "El reporte indica que el sistema de pago no está funcionando correctamente. "
        "Esto impide que los clientes finalicen su compra, lo cual tiene impacto "
        "directo en la operación del supermercado."
    ),
    "problema_pantalla": (
        "El reporte indica que la pantalla táctil no responde. Como es la única "
        "interfaz de usuario del carrito, sin ella el cliente no puede operar el sistema."
    ),
    "problema_sesion": (
        "El reporte indica que no es posible iniciar sesión en el carrito. "
        "Esto puede deberse a un problema en la base de datos local, "
        "en las credenciales del usuario o en la interfaz gráfica."
    ),
    "problema_inventario": (
        "El reporte indica una discrepancia entre los productos registrados en el "
        "sistema y los productos físicos en el carrito. Esto puede generar "
        "cobros incorrectos al cliente."
    ),
    "reporte_falla": (
        "El reporte indica una falla general del sistema. La Raspberry Pi, "
        "que es el cerebro del carrito, puede no estar respondiendo correctamente."
    ),
    "solicitud_mantenimiento": (
        "Se recibió una solicitud de mantenimiento preventivo o correctivo. "
        "Se recomienda programar una revisión técnica completa del carrito."
    ),
    "consulta_estado": (
        "Se recibió una consulta sobre el estado del sistema. "
        "Se generará un diagnóstico del estado actual del carrito."
    ),
    "desconocida": (
        "El sistema no pudo clasificar claramente la intención del reporte. "
        "Se recomienda que el cliente proporcione más detalles sobre la falla."
    ),
}


def process(agent1_output: dict, agent2_output: dict) -> dict:
    """
    Agente 3 — Genera la explicación del razonamiento del sistema experto.

    Args:
        agent1_output: Resultado del Agente 1.
        agent2_output: Resultado del Agente 2.

    Returns:
        dict con resumen narrativo, explicación detallada y validación final.
    """
    intent    = agent1_output.get("intent", "desconocida")
    cart_id   = agent1_output.get("cart_id") or "No identificado"
    component = agent2_output.get("component", "componente desconocido")
    priority  = agent2_output.get("priority", "media")
    ticket_id = agent2_output.get("ticket_id", "N/A")
    diagnosis = agent2_output.get("diagnosis", "")
    recommendation = agent2_output.get("recommendation", "")
    rules_applied  = agent2_output.get("rules_applied", [])
    confidence     = agent2_output.get("confidence", 0.0)
    chaining       = agent2_output.get("chaining_applied", False)
    previous       = agent2_output.get("previous_tickets", 0)
    all_explanations = agent2_output.get("all_explanations", [])
    category  = agent1_output.get("category", "")
    keywords  = agent1_output.get("keywords", [])

    # --- Construir resumen narrativo ---
    priority_label = PRIORITY_LABELS.get(priority, priority.upper())
    intent_explain = INTENT_EXPLANATIONS.get(intent, "")
    priority_reason = PRIORITY_REASONS.get(priority, "")

    rules_str = ", ".join(rules_applied) if rules_applied else "ninguna"

    summary = (
        f"Se recibió un reporte del carrito **{cart_id}**. "
        f"{intent_explain}\n\n"
        f"El sistema identificó el problema como: **{diagnosis}** "
        f"en el componente **{component}** ({category}).\n\n"
        f"Se aplicaron las reglas: **{rules_str}**. "
        f"La prioridad asignada es {priority_label}. "
        f"{priority_reason}\n\n"
        f"**Acción recomendada:** {recommendation}"
    )

    # --- Explicación detallada del razonamiento ---
    reasoning_steps = [
        f"1⃣ **Interpretación del mensaje:** El Agente 1 analizó el texto y detectó "
        f"la intención '{intent}' con las palabras clave: {', '.join(keywords) if keywords else 'N/A'}.",
        f"2⃣ **Consulta de historial:** Se encontraron {previous} ticket(s) previo(s) "
        f"para el carrito {cart_id}.",
        f"3⃣ **Aplicación de reglas:** El motor de inferencia evaluó {len(rules_applied)} regla(s): "
        f"{rules_str}.",
        f"4⃣ **Diagnóstico:** Se determinó que el problema es '{diagnosis}' "
        f"con una confianza del {confidence:.0%}.",
        f"5⃣ **Prioridad asignada:** {priority_label}. {priority_reason}",
    ]

    if chaining:
        reasoning_steps.append(
            " **Inferencia encadenada:** Se detectaron condiciones adicionales que "
            "activaron el escalamiento automático de la prioridad."
        )

    if previous >= 2:
        reasoning_steps.append(
            f" **Regla R8 activada:** El carrito tiene {previous} incidencias previas. "
            "Se recomienda mantenimiento preventivo urgente."
        )

    # --- Validación final ---
    validation_message = (
        f" **Ticket generado:** {ticket_id}\n"
        f"El sistema ha procesado el reporte y generado el ticket correspondiente. "
        f"Por favor, confirme si el diagnóstico es correcto o proporcione información adicional."
    )

    result = {
        "agent":            "Agente 3 — Supervisor / Explicador",
        "ticket_id":        ticket_id,
        "summary":          summary,
        "reasoning_steps":  reasoning_steps,
        "all_explanations": all_explanations,
        "validation_message": validation_message,
        "priority_label":   priority_label,
        "confidence":       confidence,
        "chaining_applied": chaining,
        "status":           "ok",
        "notes": (
            f"Razonamiento completo generado para ticket {ticket_id}. "
            f"Confianza del diagnóstico: {confidence:.0%}."
        ),
    }

    return result


if __name__ == "__main__":
    mock_a1 = {
        "intent": "problema_rfid",
        "category": "Identificación de productos",
        "component": "Lector RFID",
        "cart_id": "SGC-004",
        "urgency": "media",
        "keywords": ["no detecta", "rfid"],
        "raw_message": "El carrito SGC-004 no detecta productos RFID.",
    }
    mock_a2 = {
        "ticket_id": "TKT-20241201120000",
        "diagnosis": "Revisar lector RFID",
        "priority": "media",
        "component": "Lector RFID",
        "recommendation": "Verificar conexión y alimentación del lector RFID.",
        "rules_applied": ["R1", "R2"],
        "confidence": 0.75,
        "chaining_applied": False,
        "previous_tickets": 0,
        "all_explanations": [],
    }
    result = process(mock_a1, mock_a2)
    print("\n=== Resultado Agente 3 ===")
    print(f"Summary:\n{result['summary']}\n")
    print("Reasoning steps:")
    for step in result["reasoning_steps"]:
        print(f"  {step}")
