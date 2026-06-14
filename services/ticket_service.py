"""
Smart-Guard Support Center - Servicio de Tickets
Crea, guarda y consulta tickets en la base de datos.
"""

import datetime
import database as db


def _generate_ticket_id() -> str:
    """Genera un ID único de ticket basado en timestamp con microsegundos."""
    now = datetime.datetime.now()
    return f"TKT-{now.strftime('%Y%m%d%H%M%S')}{now.microsecond // 1000:03d}"


def create_ticket(
    agent1_output: dict,
    inference_output: dict,
    client_id: int,
) -> dict:
    """
    Crea y guarda un ticket en la base de datos.

    Args:
        agent1_output: Resultado del Agente 1.
        inference_output: Resultado del motor de inferencia.
        client_id: ID del cliente.

    Returns:
        dict con los datos del ticket creado.
    """
    ticket_id = _generate_ticket_id()
    rules_applied_str = ", ".join(inference_output.get("rules_applied", []))

    # Insertar ticket
    db.execute(
        """INSERT INTO tickets
           (ticket_id, client_id, cart_id, raw_message, intent, category,
            component, priority, status, diagnosis, solution, rules_applied)
           VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
        (
            ticket_id,
            client_id,
            agent1_output.get("cart_id") or "N/A",
            agent1_output.get("raw_message", ""),
            agent1_output.get("intent", "desconocida"),
            agent1_output.get("category", ""),
            inference_output.get("component", ""),
            inference_output.get("priority", "media"),
            "abierto",
            inference_output.get("diagnosis", ""),
            inference_output.get("recommendation", ""),
            rules_applied_str,
        ),
    )

    # Guardar diagnóstico
    db.execute(
        """INSERT INTO diagnostics (ticket_id, agent, result, confidence)
           VALUES (?,?,?,?)""",
        (
            ticket_id,
            "Agente 2 — Diagnóstico",
            inference_output.get("diagnosis", ""),
            inference_output.get("confidence", 0.0),
        ),
    )

    # Guardar log de inferencias
    for rule_item in inference_output.get("rules_detail", []):
        rule = rule_item["rule"]
        db.execute(
            """INSERT INTO inference_logs
               (ticket_id, rule_id, rule_name, conditions_met, result, explanation)
               VALUES (?,?,?,?,?,?)""",
            (
                ticket_id,
                rule["id"],
                rule["name"],
                ", ".join(rule.get("conditions", [])[:3]),
                rule.get("result", ""),
                rule.get("explanation", ""),
            ),
        )

    # Guardar en historial de mantenimiento
    db.execute(
        """INSERT INTO maintenance_history (cart_id, ticket_id, action, notes)
           VALUES (?,?,?,?)""",
        (
            agent1_output.get("cart_id") or "N/A",
            ticket_id,
            f"Ticket generado: {inference_output.get('diagnosis', '')}",
            inference_output.get("recommendation", ""),
        ),
    )

    ticket = {
        "ticket_id":    ticket_id,
        "client_id":    client_id,
        "cart_id":      agent1_output.get("cart_id") or "N/A",
        "intent":       agent1_output.get("intent", ""),
        "category":     agent1_output.get("category", ""),
        "component":    inference_output.get("component", ""),
        "priority":     inference_output.get("priority", "media"),
        "status":       "abierto",
        "diagnosis":    inference_output.get("diagnosis", ""),
        "solution":     inference_output.get("recommendation", ""),
        "rules_applied": rules_applied_str,
        "created_at":   datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    return ticket


def get_open_tickets_count() -> int:
    return db.get_open_tickets_count()


def get_tickets_by_cart(cart_id: str) -> list:
    return db.get_tickets_by_cart(cart_id)


def get_recent_tickets(limit: int = 20) -> list:
    return db.get_recent_tickets(limit)


def count_previous_tickets_for_cart(cart_id: str) -> int:
    """Cuenta cuántos tickets anteriores tiene el carrito."""
    if not cart_id:
        return 0
    rows = db.query(
        "SELECT COUNT(*) as cnt FROM tickets WHERE cart_id=?", (cart_id,)
    )
    return rows[0]["cnt"] if rows else 0
