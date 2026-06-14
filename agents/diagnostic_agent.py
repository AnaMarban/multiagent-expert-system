"""
Smart-Guard Support Center - Agente 2: Diagnóstico y Generación de Ticket
Responsabilidad: Recibir output del Agente 1, aplicar el motor de inferencia,
generar diagnóstico, asignar prioridad y crear el ticket en base de datos.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.motor_inferencia import run as run_inference
from services.ticket_service import (
    create_ticket,
    count_previous_tickets_for_cart,
)


def process(agent1_output: dict, client_id: int = None) -> dict:
    """
    Agente 2 — Diagnóstico y generación de ticket.

    Args:
        agent1_output: Resultado del Agente 1.
        client_id: ID del cliente en la base de datos.

    Returns:
        dict con diagnóstico, prioridad, ticket, inferencias, etc.
    """
    cart_id = agent1_output.get("cart_id")

    # 1. Revisar historial del carrito
    previous_count = count_previous_tickets_for_cart(cart_id) if cart_id else 0

    # 2. Ejecutar motor de inferencia
    inference_result = run_inference(agent1_output, previous_tickets_count=previous_count)

    # 3. Crear y guardar ticket
    used_client_id = client_id or agent1_output.get("client_id") or 1
    ticket = create_ticket(agent1_output, inference_result, used_client_id)

    # 4. Construir resultado del agente
    result = {
        "agent":            "Agente 2 — Diagnóstico y Ticket",
        "ticket_id":        ticket["ticket_id"],
        "cart_id":          ticket["cart_id"],
        "diagnosis":        inference_result["diagnosis"],
        "priority":         inference_result["priority"],
        "component":        inference_result["component"],
        "recommendation":   inference_result["recommendation"],
        "rules_applied":    inference_result["rules_applied"],
        "rules_detail":     inference_result["rules_detail"],
        "confidence":       inference_result["confidence"],
        "chaining_applied": inference_result["chaining_applied"],
        "previous_tickets": previous_count,
        "all_explanations": inference_result["all_explanations"],
        "ticket":           ticket,
        "status":           "ok",
        "notes": (
            f"Ticket {ticket['ticket_id']} creado. "
            f"Prioridad: {inference_result['priority'].upper()}. "
            f"Reglas aplicadas: {', '.join(inference_result['rules_applied'])}."
        ),
    }

    return result


if __name__ == "__main__":
    # Prueba directa del Agente 2
    import sys, os
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    import database
    database.init_database()

    mock_agent1 = {
        "intent": "problema_rfid",
        "category": "Identificación de productos",
        "component": "Lector RFID",
        "cart_id": "SGC-004",
        "urgency": "media",
        "keywords": ["no detecta", "rfid"],
        "raw_message": "El carrito SGC-004 no detecta productos RFID.",
        "client_id": 1,
    }

    result = process(mock_agent1, client_id=1)
    print("\n=== Resultado Agente 2 ===")
    for k, v in result.items():
        if k != "rules_detail":
            print(f"  {k}: {v}")
