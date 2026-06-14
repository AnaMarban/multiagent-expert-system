"""
Smart-Guard Support Center - Servicio de Reportes y Métricas
"""

import database as db


def get_dashboard_metrics() -> dict:
    """Retorna métricas generales para el panel principal."""
    open_tickets = db.get_open_tickets_count()
    total_carts = db.get_carts_count()
    critical = db.get_critical_tickets_count()

    # Tiempo estimado de atención (heurística simple)
    if critical > 0:
        estimated_time = "< 2 horas"
    elif open_tickets > 5:
        estimated_time = "2-4 horas"
    elif open_tickets > 0:
        estimated_time = "4-8 horas"
    else:
        estimated_time = "Sin pendientes"

    total_tickets = db.query("SELECT COUNT(*) as cnt FROM tickets")[0]["cnt"]
    resolved = db.query(
        "SELECT COUNT(*) as cnt FROM tickets WHERE status IN ('resuelto','cerrado')"
    )[0]["cnt"]

    return {
        "open_tickets":     open_tickets,
        "total_carts":      total_carts,
        "critical_tickets": critical,
        "estimated_time":   estimated_time,
        "total_tickets":    total_tickets,
        "resolved_tickets": resolved,
    }


def get_tickets_history(limit: int = 30) -> list:
    """Retorna historial de tickets para mostrar en tabla."""
    rows = db.get_recent_tickets(limit)
    return rows


def get_inference_logs_for_ticket(ticket_id: str) -> list:
    """Retorna los logs de inferencia de un ticket."""
    return db.get_inference_logs_by_ticket(ticket_id)


def get_tickets_by_priority() -> dict:
    """Retorna conteo de tickets por prioridad."""
    rows = db.query(
        """SELECT priority, COUNT(*) as cnt
           FROM tickets WHERE status='abierto'
           GROUP BY priority"""
    )
    return {r["priority"]: r["cnt"] for r in rows}


def get_most_affected_carts(limit: int = 5) -> list:
    """Retorna los carritos con más incidencias."""
    return db.query(
        """SELECT cart_id, COUNT(*) as total
           FROM tickets GROUP BY cart_id
           ORDER BY total DESC LIMIT ?""",
        (limit,),
    )


def get_solutions_catalog() -> list:
    """Retorna el catálogo de soluciones conocidas."""
    return db.query("SELECT * FROM solutions ORDER BY problem_category")
