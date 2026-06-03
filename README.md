# Smart-Guard Expert

## Sistema Experto Multiagente para Seguridad y Diagnóstico del Smart-Guard Cart

Smart-Guard Expert es un prototipo local desarrollado en Python que simula el módulo inteligente de decisión de un carrito de compras inteligente.

El sistema analiza eventos relacionados con productos detectados, estado de pago, zona del carrito y nivel de batería. A partir de esta información, aplica reglas de inferencia y genera una explicación de las decisiones tomadas.

---

## Objetivo

Desarrollar un sistema experto moderno basado en agentes inteligentes que permita analizar eventos del Smart-Guard Cart, detectar irregularidades, generar alertas y explicar el razonamiento utilizado.

---

## Relación con Smart-Guard Cart

Este proyecto se adapta al concepto del Smart-Guard Cart, un carrito inteligente diseñado para mejorar la seguridad y el control de productos en tiendas o supermercados.

Smart-Guard Expert funciona como el módulo lógico del sistema, encargado de tomar decisiones como:

- Detectar productos no registrados.
- Verificar si el pago fue completado.
- Identificar eventos sospechosos en la zona de salida.
- Recomendar carga del carrito cuando la batería es baja.
- Explicar las decisiones tomadas mediante reglas de inferencia.

---

## Agentes implementados

### 1. Agente de Monitoreo del Carrito

Recibe y organiza los datos del evento:

- ID del carrito.
- Producto detectado por RFID.
- Estado de registro del producto.
- Estado del pago.
- Zona actual del carrito.
- Nivel de batería.

### 2. Agente de Inferencia y Seguridad

Aplica reglas de inferencia para determinar si existe una irregularidad o si el carrito puede continuar operando normalmente.

### 3. Agente Supervisor / Explicador

Genera una explicación clara del razonamiento utilizado por el sistema. Este agente permite cumplir con el requisito de explicabilidad.

---

## Reglas de inferencia iniciales

```txt
R1:
IF producto_detectado = verdadero
AND producto_registrado = falso
THEN generar_alerta_producto_no_registrado

R2:
IF zona = salida
AND pago_completado = falso
THEN bloquear_carrito_temporalmente

R3:
IF bateria < 20
THEN recomendar_estacion_de_carga

R4:
IF producto_registrado = verdadero
AND pago_completado = verdadero
THEN permitir_operacion_normal

R5:
IF producto_detectado = falso
THEN solicitar_nueva_lectura_RFID