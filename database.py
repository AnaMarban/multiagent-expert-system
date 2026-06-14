"""
Smart-Guard Support Center - Gestión de Base de Datos SQLite
"""

import sqlite3
import os
from datetime import datetime
from config import DB_PATH


def get_connection():
    """Retorna una conexión a la base de datos SQLite."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_database():
    """Inicializa la base de datos, crea tablas e inserta datos iniciales."""
    conn = get_connection()
    cursor = conn.cursor()

    # --- TABLAS ---
    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            contact TEXT,
            city TEXT,
            active INTEGER DEFAULT 1,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS carts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cart_id TEXT NOT NULL UNIQUE,
            client_id INTEGER,
            model TEXT DEFAULT 'SGC-v1',
            status TEXT DEFAULT 'activo',
            location TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (client_id) REFERENCES clients(id)
        );

        CREATE TABLE IF NOT EXISTS components (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT,
            description TEXT,
            critical INTEGER DEFAULT 0
        );

        CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticket_id TEXT NOT NULL UNIQUE,
            client_id INTEGER,
            cart_id TEXT,
            raw_message TEXT,
            intent TEXT,
            category TEXT,
            component TEXT,
            priority TEXT,
            status TEXT DEFAULT 'abierto',
            diagnosis TEXT,
            solution TEXT,
            rules_applied TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (client_id) REFERENCES clients(id)
        );

        CREATE TABLE IF NOT EXISTS diagnostics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticket_id TEXT,
            agent TEXT,
            result TEXT,
            confidence REAL DEFAULT 0.0,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS inference_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticket_id TEXT,
            rule_id TEXT,
            rule_name TEXT,
            conditions_met TEXT,
            result TEXT,
            explanation TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS maintenance_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cart_id TEXT,
            ticket_id TEXT,
            action TEXT,
            technician TEXT DEFAULT 'Sistema Experto',
            notes TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS solutions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            problem_category TEXT,
            component TEXT,
            solution_text TEXT,
            steps TEXT,
            estimated_time TEXT,
            requires_technician INTEGER DEFAULT 0
        );
    """)

    # --- DATOS INICIALES (solo si no existen) ---
    # Clientes
    clients = [
        ("Supermarket La Central", "soporte@lacentral.com", "Guadalajara"),
        ("Walmart Norte", "ti@walmartnorte.com", "Zapopan"),
        ("Chedraui Sur", "sistemas@chedraui.com", "Tlaquepaque"),
        ("HEB Demo", "demo@heb.com", "Tonala"),
    ]
    for c in clients:
        cursor.execute(
            "INSERT OR IGNORE INTO clients (name, contact, city) VALUES (?,?,?)", c
        )

    # Carritos
    carts = [
        ("SGC-001", 1), ("SGC-002", 1), ("SGC-003", 2),
        ("SGC-004", 2), ("SGC-005", 3), ("SGC-006", 3), ("SGC-007", 4),
    ]
    for cart_id, client_id in carts:
        cursor.execute(
            "INSERT OR IGNORE INTO carts (cart_id, client_id) VALUES (?,?)",
            (cart_id, client_id),
        )

    # Componentes
    components = [
        ("Raspberry Pi 4",  "Procesamiento", "Unidad central de cómputo", 1),
        ("Lector RFID",     "Identificación","Lector de etiquetas RFID 13.56MHz", 1),
        ("Pantalla táctil", "Interfaz",      "Display táctil 7 pulgadas", 0),
        ("Módulo de batería","Energía",      "Batería recargable Li-Ion", 1),
        ("Dock magnético",  "Carga",         "Sistema de carga por contacto magnético", 0),
        ("Sistema de pago", "Transacciones", "Módulo NFC/QR para validación de pago", 1),
        ("Base de datos local","Software",   "SQLite embebido en Raspberry Pi", 0),
        ("Módulo de red",   "Conectividad",  "WiFi/Ethernet para sincronización", 0),
        ("Tags RFID",       "Identificación","Etiquetas RFID adheridas a productos", 0),
    ]
    for comp in components:
        cursor.execute(
            "INSERT OR IGNORE INTO components (name,category,description,critical) VALUES (?,?,?,?)",
            comp,
        )

    # Soluciones base
    solutions_data = [
        ("Identificación de productos","Lector RFID",
         "Revisar lector RFID, conexión y alimentación",
         "1. Verificar conexión USB/SPI del lector\n2. Revisar alimentación 3.3V\n3. Limpiar antena lectora\n4. Reiniciar servicio RFID",
         "30-60 min", 0),
        ("Gestión de sesión","Pantalla táctil",
         "Revisar pantalla, usuario registrado y base de datos local",
         "1. Verificar integridad de BD local\n2. Reiniciar interfaz\n3. Validar credenciales de usuario",
         "15-30 min", 0),
        ("Sistema de pago","Sistema de pago",
         "Revisar módulo de pago o generar código alternativo",
         "1. Verificar conectividad\n2. Reiniciar módulo NFC\n3. Usar código alternativo de validación",
         "20-45 min", 1),
        ("Energía y carga","Módulo de batería",
         "Retornar al dock magnético o revisar sistema de carga",
         "1. Llevar carrito a bahía de carga\n2. Verificar alineación\n3. Revisar contactos magnéticos",
         "10-20 min", 0),
        ("Pantalla e interfaz","Pantalla táctil",
         "Revisar conexión de pantalla, reiniciar interfaz y validar alimentación",
         "1. Verificar cable display\n2. Reiniciar servicio gráfico\n3. Revisar alimentación 5V",
         "20-40 min", 0),
    ]
    for s in solutions_data:
        cursor.execute(
            """INSERT OR IGNORE INTO solutions
               (problem_category,component,solution_text,steps,estimated_time,requires_technician)
               VALUES (?,?,?,?,?,?)""",
            s,
        )

    conn.commit()
    conn.close()
    print(f"[DB] Base de datos inicializada en: {DB_PATH}")


def query(sql, params=()):
    """Ejecuta una consulta SELECT y retorna filas como dicts."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(sql, params)
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows


def execute(sql, params=()):
    """Ejecuta INSERT/UPDATE/DELETE y retorna lastrowid."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(sql, params)
    conn.commit()
    last_id = cursor.lastrowid
    conn.close()
    return last_id


def get_clients():
    return query("SELECT * FROM clients WHERE active=1 ORDER BY name")


def get_carts(client_id=None):
    if client_id:
        return query("SELECT * FROM carts WHERE client_id=? ORDER BY cart_id", (client_id,))
    return query("SELECT * FROM carts ORDER BY cart_id")


def get_open_tickets_count():
    result = query("SELECT COUNT(*) as cnt FROM tickets WHERE status='abierto'")
    return result[0]["cnt"] if result else 0


def get_carts_count():
    result = query("SELECT COUNT(*) as cnt FROM carts")
    return result[0]["cnt"] if result else 0


def get_critical_tickets_count():
    result = query("SELECT COUNT(*) as cnt FROM tickets WHERE priority='critica' AND status='abierto'")
    return result[0]["cnt"] if result else 0


def get_recent_tickets(limit=20):
    return query(
        """SELECT t.*, c.name as client_name
           FROM tickets t LEFT JOIN clients c ON t.client_id=c.id
           ORDER BY t.created_at DESC LIMIT ?""",
        (limit,),
    )


def get_tickets_by_cart(cart_id):
    return query("SELECT * FROM tickets WHERE cart_id=? ORDER BY created_at DESC", (cart_id,))


def get_inference_logs_by_ticket(ticket_id):
    return query("SELECT * FROM inference_logs WHERE ticket_id=? ORDER BY id", (ticket_id,))


if __name__ == "__main__":
    init_database()
    print("Clientes:", [c["name"] for c in get_clients()])
    print("Carritos:", [c["cart_id"] for c in get_carts()])
