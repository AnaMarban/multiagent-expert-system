"""
Smart-Guard Support Center - Base de Conocimiento: Reglas de Inferencia
Motor de reglas tipo IF/THEN para el sistema experto.
"""

RULES = [
    {
        "id": "R1",
        "name": "Falla de RFID detectada",
        "conditions": ["rfid", "no detecta", "lector", "lectura", "etiqueta", "tag"],
        "intent_match": ["problema_rfid"],
        "result": "Identificación de productos",
        "priority": "media",
        "component": "Lector RFID",
        "recommendation": "Revisar lector RFID, su conexión y alimentación eléctrica.",
        "explanation": (
            "Se detectaron palabras clave relacionadas con fallas en la lectura RFID. "
            "El sistema clasifica esto como un problema de identificación de productos."
        ),
    },
    {
        "id": "R2",
        "name": "Carrito activo sin lectura RFID",
        "conditions": ["no detecta", "productos", "rfid", "activo"],
        "intent_match": ["problema_rfid"],
        "result": "Revisar lector RFID",
        "priority": "media",
        "component": "Lector RFID",
        "recommendation": (
            "Verificar conexión física del lector RFID, revisar alimentación 3.3V, "
            "limpiar antena y reiniciar el servicio RFID en la Raspberry Pi."
        ),
        "explanation": (
            "El carrito está operativo pero no detecta productos. "
            "Si el carrito está activo y el lector falla, la causa más probable es "
            "un problema de conexión o alimentación del módulo RFID."
        ),
    },
    {
        "id": "R3",
        "name": "Falla al iniciar sesión",
        "conditions": ["iniciar sesión", "no permite", "sesión", "login", "acceso", "usuario"],
        "intent_match": ["problema_sesion"],
        "result": "Gestión de sesión",
        "priority": "media",
        "component": "Pantalla táctil",
        "recommendation": (
            "Revisar integridad de la base de datos local, validar que el usuario esté registrado "
            "y reiniciar la interfaz de usuario."
        ),
        "explanation": (
            "La falla al iniciar sesión puede deberse a un problema en la base de datos local, "
            "credenciales incorrectas o un fallo en la pantalla táctil."
        ),
    },
    {
        "id": "R4",
        "name": "Discrepancia en total de compra",
        "conditions": ["total", "no coincide", "productos físicos", "diferencia", "lista", "virtual"],
        "intent_match": ["problema_inventario"],
        "result": "Validación de inventario",
        "priority": "alta",
        "component": "Lector RFID",
        "recommendation": (
            "Solicitar validación manual de los productos en el carrito y revisar "
            "las lecturas RFID recientes en el log del sistema."
        ),
        "explanation": (
            "Una discrepancia entre el total virtual y los productos físicos indica "
            "lecturas RFID incorrectas, productos no vinculados o eliminaciones no registradas."
        ),
    },
    {
        "id": "R5",
        "name": "Batería baja fuera de bahía",
        "conditions": ["batería baja", "baja", "bateria", "carga", "fuera", "no carga"],
        "intent_match": ["problema_bateria"],
        "result": "Energía insuficiente",
        "priority": "media",
        "component": "Módulo de batería",
        "recommendation": "Regresar el carrito al dock magnético de carga inmediatamente.",
        "explanation": (
            "La batería está baja y el carrito no está en la bahía de carga. "
            "Si no se recarga pronto, el carrito dejará de funcionar."
        ),
    },
    {
        "id": "R6",
        "name": "Batería baja en bahía de carga",
        "conditions": ["batería baja", "bahía", "dock", "no carga", "cargando", "magnético"],
        "intent_match": ["problema_bateria"],
        "result": "Falla en sistema de carga",
        "priority": "alta",
        "component": "Dock magnético",
        "recommendation": (
            "Revisar alineación del carrito en la bahía, limpiar contactos magnéticos "
            "y verificar la fuente de alimentación del dock."
        ),
        "explanation": (
            "Si el carrito está en la bahía pero la batería no carga, "
            "el problema está en el dock magnético o en los contactos de carga."
        ),
    },
    {
        "id": "R7",
        "name": "Falla en validación de pago",
        "conditions": ["pago", "no valida", "finalizar", "compra", "cobro", "transacción", "nfc"],
        "intent_match": ["problema_pago"],
        "result": "Sistema de pago",
        "priority": "alta",
        "component": "Sistema de pago",
        "recommendation": (
            "Verificar conectividad del módulo de pago, reiniciar el servicio NFC "
            "y ofrecer código alternativo de validación manual."
        ),
        "explanation": (
            "La falla en el pago impide que el cliente complete su compra. "
            "Esto tiene impacto directo en la operación del supermercado."
        ),
    },
    {
        "id": "R8",
        "name": "Múltiples tickets del mismo carrito",
        "conditions": ["reincidente", "repetido", "mismo carrito", "varias veces", "múltiple"],
        "intent_match": [],
        "result": "Mantenimiento preventivo urgente",
        "priority": "alta",
        "component": "Hardware general",
        "recommendation": (
            "Programar revisión técnica completa del carrito. "
            "El historial de fallas repetidas indica un problema de fondo."
        ),
        "explanation": (
            "Se detectaron múltiples incidencias previas en el mismo carrito. "
            "Esto activa la regla de escalamiento de prioridad."
        ),
    },
    {
        "id": "R9",
        "name": "Raspberry Pi sin respuesta",
        "conditions": ["raspberry", "pi", "no responde", "apagada", "sistema", "colgada", "bloqueada"],
        "intent_match": ["reporte_falla"],
        "result": "Falla en unidad de procesamiento",
        "priority": "critica",
        "component": "Raspberry Pi 4",
        "recommendation": (
            "Realizar reinicio forzado de la Raspberry Pi, revisar alimentación 5V/3A "
            "y verificar integridad de la tarjeta SD."
        ),
        "explanation": (
            "La Raspberry Pi es el cerebro del carrito. Si no responde, "
            "el carrito queda completamente fuera de servicio."
        ),
    },
    {
        "id": "R10",
        "name": "Tags RFID duplicados",
        "conditions": ["duplicado", "mismo producto", "varias veces", "repite", "doble lectura", "antirebote"],
        "intent_match": ["problema_rfid"],
        "result": "Filtro antirebote RFID",
        "priority": "media",
        "component": "Lector RFID",
        "recommendation": (
            "Aplicar o ajustar el filtro antirebote en el código de lectura RFID "
            "y revisar la distancia entre el lector y los productos."
        ),
        "explanation": (
            "La lectura duplicada ocurre cuando el lector detecta el mismo tag "
            "múltiples veces en poco tiempo. Se requiere implementar un filtro temporal."
        ),
    },
    {
        "id": "R11",
        "name": "Producto no registrado en base de datos",
        "conditions": ["no existe", "no encontrado", "base de datos", "inventario", "producto desconocido", "no vinculado"],
        "intent_match": ["problema_inventario"],
        "result": "Alerta de inventario",
        "priority": "baja",
        "component": "Base de datos local",
        "recommendation": (
            "Registrar el producto en el sistema de inventario del supermercado "
            "y sincronizar la base de datos del carrito."
        ),
        "explanation": (
            "El producto fue escaneado correctamente por el RFID, "
            "pero no existe en la base de datos local del carrito."
        ),
    },
    {
        "id": "R12",
        "name": "Incidencia masiva de carritos",
        "conditions": ["tres carritos", "varios carritos", "todos los carritos", "múltiples carritos", "sistema general"],
        "intent_match": [],
        "result": "Incidencia crítica del sistema",
        "priority": "critica",
        "component": "Hardware general",
        "recommendation": (
            "Activar protocolo de incidencia crítica. Revisar infraestructura de red, "
            "servidor central y fuente de alimentación general."
        ),
        "explanation": (
            "Cuando más de tres carritos presentan la misma falla simultáneamente, "
            "se clasifica como incidencia crítica que puede afectar toda la operación."
        ),
    },
    {
        "id": "R13",
        "name": "Pantalla táctil sin respuesta",
        "conditions": ["pantalla", "no responde", "táctil", "congelada", "negra", "no enciende", "display"],
        "intent_match": ["problema_pantalla"],
        "result": "Pantalla e interfaz",
        "priority": "media",
        "component": "Pantalla táctil",
        "recommendation": (
            "Revisar el cable del display, reiniciar el servicio gráfico con "
            "`sudo systemctl restart display-manager` y verificar la alimentación 5V."
        ),
        "explanation": (
            "La pantalla es la interfaz principal del carrito. "
            "Si no responde, el usuario no puede operar el sistema."
        ),
    },
    {
        "id": "R14",
        "name": "Dock magnético sin carga",
        "conditions": ["dock", "magnético", "no carga", "bahía", "cargador", "contactos"],
        "intent_match": ["problema_bateria"],
        "result": "Falla en dock de carga",
        "priority": "alta",
        "component": "Dock magnético",
        "recommendation": (
            "Verificar alineación del carrito en la bahía, revisar y limpiar los contactos "
            "magnéticos y comprobar la fuente de alimentación del dock."
        ),
        "explanation": (
            "El dock magnético es el sistema de recarga del carrito. "
            "Una falla aquí deja el carrito sin energía a largo plazo."
        ),
    },
    {
        "id": "R15",
        "name": "Sistema con lentitud o bloqueos",
        "conditions": ["lento", "lentitud", "tarda", "bloqueo", "freezing", "lento", "no responde rápido"],
        "intent_match": ["reporte_falla"],
        "result": "Rendimiento del sistema",
        "priority": "baja",
        "component": "Raspberry Pi 4",
        "recommendation": (
            "Revisar procesos activos en la Raspberry Pi, liberar memoria RAM "
            "y reiniciar los servicios locales del sistema Smart-Guard."
        ),
        "explanation": (
            "La lentitud puede deberse a procesos acumulados en la Raspberry Pi o "
            "a una tarjeta SD con bajo rendimiento."
        ),
    },
]


def get_all_rules():
    """Retorna todas las reglas del sistema."""
    return RULES


def get_rule_by_id(rule_id):
    """Retorna una regla específica por su ID."""
    for rule in RULES:
        if rule["id"] == rule_id:
            return rule
    return None
