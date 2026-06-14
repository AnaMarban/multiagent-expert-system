"""
Smart-Guard Support Center - Conocimiento General del Producto Smart-Guard Cart
Base de conocimiento estática del sistema experto.
"""

PRODUCT_INFO = {
    "name": "Smart-Guard Cart",
    "version": "Prototipo v1.0",
    "description": (
        "Carrito de compras inteligente diseñado para optimizar, automatizar y asegurar "
        "el proceso de compra en supermercados. Utiliza tecnología RFID, Raspberry Pi 4 "
        "e interfaces táctiles para ofrecer una experiencia de compra autónoma."
    ),
    "components": [
        {
            "name": "Raspberry Pi 4",
            "role": "Unidad central de procesamiento",
            "details": "Corre el sistema operativo y los servicios del carrito. 4GB RAM, 32GB SD.",
        },
        {
            "name": "Lector RFID",
            "role": "Identificación de productos",
            "details": "Detecta etiquetas RFID a 13.56MHz. Rango de lectura: ~10cm.",
        },
        {
            "name": "Pantalla táctil",
            "role": "Interfaz de usuario local",
            "details": "Display táctil de 7 pulgadas. Muestra lista de productos, totales y opciones.",
        },
        {
            "name": "Módulo de batería",
            "role": "Fuente de energía",
            "details": "Batería Li-Ion de alta capacidad. Autonomía aprox. 8 horas de uso continuo.",
        },
        {
            "name": "Dock magnético",
            "role": "Sistema de carga inalámbrica",
            "details": "Carga por contacto magnético al devolver el carrito a la bahía.",
        },
        {
            "name": "Sistema de pago",
            "role": "Validación de transacciones",
            "details": "Módulo NFC/QR para validar pago sin pasar por caja.",
        },
        {
            "name": "Base de datos local",
            "role": "Persistencia de datos",
            "details": "SQLite embebido en la Raspberry Pi con catálogo de productos.",
        },
        {
            "name": "Módulo de red",
            "role": "Conectividad",
            "details": "WiFi 802.11ac para sincronización con servidor central del supermercado.",
        },
        {
            "name": "Tags RFID",
            "role": "Etiquetado de productos",
            "details": "Etiquetas adhesivas RFID adheridas a cada producto del inventario.",
        },
    ],
    "operation_flow": [
        {
            "step": 1,
            "title": "Inicio de sesión y vinculación",
            "description": (
                "El cliente se identifica en la pantalla táctil con su número de socio o QR. "
                "El carrito queda vinculado a la sesión del usuario."
            ),
        },
        {
            "step": 2,
            "title": "Lectura y conteo automático",
            "description": (
                "Al colocar productos en el carrito, el lector RFID los detecta automáticamente. "
                "La lista y el total se actualizan en tiempo real en la pantalla."
            ),
        },
        {
            "step": 3,
            "title": "Gestión de bajas (devolución)",
            "description": (
                "Si el cliente retira un producto, el sistema lo elimina de la lista "
                "y ajusta el total automáticamente."
            ),
        },
        {
            "step": 4,
            "title": "Pago autónomo y salida",
            "description": (
                "El cliente valida el pago desde la pantalla (NFC, QR o código). "
                "El sistema genera un comprobante y el cliente sale sin pasar por caja."
            ),
        },
        {
            "step": 5,
            "title": "Retorno a bahía de carga",
            "description": (
                "Al devolver el carrito, se coloca en la bahía magnética. "
                "El sistema inicia carga automática y cierra la sesión."
            ),
        },
    ],
    "customer_benefits": [
        "Cero filas en caja: pago directo desde el carrito.",
        "Control de presupuesto en tiempo real.",
        "Experiencia de compra fluida y moderna.",
        "Reducción del tiempo de compra hasta un 40%.",
        "Historial de compras disponible en la app.",
    ],
    "store_benefits": [
        "Inventario en tiempo real durante la compra.",
        "Optimización del personal de caja.",
        "Seguridad avanzada anti-hurto.",
        "Datos de comportamiento de compra.",
        "Reducción de errores en precios.",
    ],
    "common_failures": [
        {
            "failure": "RFID no detecta productos",
            "frequency": "Alta",
            "causes": ["Lector desconectado", "Tag dañado o incompatible", "Producto fuera de rango"],
            "quick_fix": "Verificar conexión del lector y limpiar antena.",
        },
        {
            "failure": "Tags duplicados",
            "frequency": "Media",
            "causes": ["Sin filtro antirebote", "Producto muy cercano al lector"],
            "quick_fix": "Ajustar filtro temporal de lectura (debounce).",
        },
        {
            "failure": "Producto no vinculado en BD",
            "frequency": "Media",
            "causes": ["Tag no registrado en inventario", "BD no sincronizada"],
            "quick_fix": "Registrar el producto y sincronizar base de datos.",
        },
        {
            "failure": "Pantalla no responde",
            "frequency": "Baja",
            "causes": ["Servicio gráfico caído", "Cable display suelto", "Alimentación insuficiente"],
            "quick_fix": "Reiniciar servicio de display manager.",
        },
        {
            "failure": "Pago no validado",
            "frequency": "Media",
            "causes": ["Sin conectividad", "Módulo NFC fallo", "Error en servidor de pagos"],
            "quick_fix": "Verificar WiFi y reiniciar módulo de pago.",
        },
        {
            "failure": "Batería baja",
            "frequency": "Alta",
            "causes": ["Carrito no regresado a bahía", "Dock magnético fallo", "Batería degradada"],
            "quick_fix": "Devolver carrito a bahía de carga.",
        },
        {
            "failure": "Dock sin carga",
            "frequency": "Baja",
            "causes": ["Mala alineación", "Contactos sucios", "Falla en fuente de alimentación"],
            "quick_fix": "Limpiar contactos y verificar alineación del carrito.",
        },
        {
            "failure": "Diferencia en lista vs físico",
            "frequency": "Media",
            "causes": ["Lecturas duplicadas", "Productos no registrados", "Bajas no procesadas"],
            "quick_fix": "Solicitar validación manual y revisar log de lecturas.",
        },
        {
            "failure": "Raspberry Pi sin respuesta",
            "frequency": "Baja",
            "causes": ["Sobrecalentamiento", "Alimentación insuficiente", "SD dañada", "Proceso colgado"],
            "quick_fix": "Reinicio forzado y verificar alimentación.",
        },
    ],
}


def get_product_info():
    return PRODUCT_INFO


def get_common_failures():
    return PRODUCT_INFO["common_failures"]


def get_operation_flow():
    return PRODUCT_INFO["operation_flow"]


def get_component_info(component_name):
    for c in PRODUCT_INFO["components"]:
        if component_name.lower() in c["name"].lower():
            return c
    return None
