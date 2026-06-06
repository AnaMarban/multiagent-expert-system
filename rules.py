def evaluate_cart_rules(producto_detectado, producto_registrado, pago_completado, zona, bateria):
    reglas_activadas = []
    decisiones = []
    explicaciones = []

    if producto_detectado and not producto_registrado:
        reglas_activadas.append("R1: Producto detectado físicamente pero no registrado en la compra.")
        decisiones.append("Generar alerta de producto no registrado.")
        explicaciones.append(
            "El sistema detectó un producto en el carrito que no aparece en la lista registrada. "
            "Esto puede indicar que el cliente olvidó escanear el producto o que existe una irregularidad."
        )

    if zona == "Salida" and not pago_completado:
        reglas_activadas.append("R2: Carrito ubicado en zona de salida sin pago completado.")
        decisiones.append("Bloquear carrito temporalmente.")
        explicaciones.append(
            "El carrito se encuentra en la zona de salida y el pago aún no ha sido confirmado. "
            "Por seguridad, se recomienda bloquear el carrito hasta validar la compra."
        )

    if bateria < 20:
        reglas_activadas.append("R3: Batería baja.")
        decisiones.append("Enviar carrito a estación de carga.")
        explicaciones.append(
            "La batería del carrito está por debajo del nivel mínimo recomendado. "
            "El sistema sugiere llevarlo a una estación de carga para evitar fallas durante el uso."
        )

    if producto_registrado and pago_completado and zona != "Salida":
        reglas_activadas.append("R4: Producto registrado y pago completado correctamente.")
        decisiones.append("Permitir operación normal.")
        explicaciones.append(
            "El producto está registrado en la compra y el pago fue confirmado. "
            "No se detectan irregularidades en este evento."
        )

    if not producto_detectado:
        reglas_activadas.append("R5: No se detectó producto físico.")
        decisiones.append("Solicitar nueva lectura del sensor RFID.")
        explicaciones.append(
            "El sistema no recibió información de producto físico. "
            "Esto puede deberse a una falla de lectura RFID o a que el carrito está vacío."
        )

    if not decisiones:
        decisiones.append("Continuar monitoreo.")
        explicaciones.append(
            "No se detectó una condición crítica. El sistema continuará supervisando el carrito."
        )

    return {
        "reglas_activadas": reglas_activadas,
        "decisiones": decisiones,
        "explicaciones": explicaciones
    }