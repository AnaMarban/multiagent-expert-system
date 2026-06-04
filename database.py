import sqlite3
from pathlib import Path


DB_PATH = Path("database/smart_guard.db")


def get_connection():
    return sqlite3.connect(DB_PATH)


def create_tables():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            codigo_rfid TEXT NOT NULL UNIQUE,
            precio REAL NOT NULL,
            categoria TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS eventos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            carrito_id TEXT NOT NULL,
            producto_detectado TEXT,
            producto_registrado INTEGER NOT NULL,
            pago_completado INTEGER NOT NULL,
            zona TEXT NOT NULL,
            bateria INTEGER NOT NULL,
            decision TEXT NOT NULL,
            explicacion TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


def insert_initial_products():
    connection = get_connection()
    cursor = connection.cursor()

    productos = [
        ("Leche 1L", "RFID001", 28.50, "Lácteos"),
        ("Pan de caja", "RFID002", 45.00, "Panadería"),
        ("Cereal", "RFID003", 62.00, "Abarrotes"),
        ("Shampoo", "RFID004", 89.90, "Higiene"),
        ("Detergente", "RFID005", 75.50, "Limpieza"),
        ("Atún en lata", "RFID006", 22.00, "Abarrotes"),
        ("Jabón corporal", "RFID007", 35.00, "Higiene"),
        ("Refresco 2L", "RFID008", 39.00, "Bebidas")
    ]

    for producto in productos:
        cursor.execute("""
            INSERT OR IGNORE INTO productos (nombre, codigo_rfid, precio, categoria)
            VALUES (?, ?, ?, ?)
        """, producto)

    connection.commit()
    connection.close()


def get_products():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT nombre, codigo_rfid, precio, categoria FROM productos")
    productos = cursor.fetchall()

    connection.close()
    return productos


def save_event(carrito_id, producto_detectado, producto_registrado, pago_completado, zona, bateria, decision, explicacion):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO eventos (
            carrito_id,
            producto_detectado,
            producto_registrado,
            pago_completado,
            zona,
            bateria,
            decision,
            explicacion
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        carrito_id,
        producto_detectado,
        int(producto_registrado),
        int(pago_completado),
        zona,
        bateria,
        decision,
        explicacion
    ))

    connection.commit()
    connection.close()


def get_events():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT carrito_id, producto_detectado, producto_registrado, pago_completado, zona, bateria, decision, explicacion
        FROM eventos
        ORDER BY id DESC
    """)

    eventos = cursor.fetchall()
    connection.close()
    return eventos


def initialize_database():
    create_tables()
    insert_initial_products()