import streamlit as st

from database.database import (
    initialize_database,
    get_products,
    save_event,
    get_events
)

from agents.agents import (
    MonitoringAgent,
    SecurityInferenceAgent,
    SupervisorAgent
)


initialize_database()

st.set_page_config(
    page_title="Smart-Guard Expert",
    page_icon="🛒",
    layout="wide"
)

st.title("Smart-Guard Expert")
st.subheader("Sistema Experto Multiagente para Seguridad y Diagnóstico del Smart-Guard Cart")

st.write("""
Este prototipo simula el módulo inteligente de decisión del Smart-Guard Cart.
El sistema analiza eventos del carrito, aplica reglas de inferencia y explica las decisiones tomadas.
""")

st.divider()

menu = st.sidebar.radio(
    "Menú principal",
    [
        "Simular evento del carrito",
        "Productos registrados",
        "Historial de eventos",
        "Acerca del sistema"
    ]
)

if menu == "Simular evento del carrito":
    st.header("Simulación de evento del carrito")

    col1, col2 = st.columns(2)

    with col1:
        carrito_id = st.text_input("ID del carrito", value="CART-001")

        productos = get_products()
        nombres_productos = ["Ninguno"] + [producto[0] for producto in productos]

        producto_seleccionado = st.selectbox(
            "Producto detectado por RFID",
            nombres_productos
        )

        producto_detectado = None if producto_seleccionado == "Ninguno" else producto_seleccionado

        producto_registrado = st.checkbox("El producto está registrado en la compra")
        pago_completado = st.checkbox("El pago fue completado")

    with col2:
        zona = st.selectbox(
            "Zona actual del carrito",
            ["Pasillo", "Caja", "Salida", "Estación de carga"]
        )

        bateria = st.slider(
            "Nivel de batería del carrito",
            min_value=0,
            max_value=100,
            value=75
        )

    st.divider()

    if st.button("Analizar evento"):
        monitoring_agent = MonitoringAgent()
        inference_agent = SecurityInferenceAgent()
        supervisor_agent = SupervisorAgent()

        cart_data = monitoring_agent.analyze_input(
            carrito_id=carrito_id,
            producto_detectado=producto_detectado,
            producto_registrado=producto_registrado,
            pago_completado=pago_completado,
            zona=zona,
            bateria=bateria
        )

        inference_result = inference_agent.evaluate_event(cart_data)
        final_report = supervisor_agent.generate_report(cart_data, inference_result)

        main_decision = inference_result["decisiones"][0]
        main_explanation = inference_result["explicaciones"][0]

        save_event(
            carrito_id=carrito_id,
            producto_detectado=producto_detectado if producto_detectado else "Ninguno",
            producto_registrado=producto_registrado,
            pago_completado=pago_completado,
            zona=zona,
            bateria=bateria,
            decision=main_decision,
            explicacion=main_explanation
        )

        st.success("Evento analizado correctamente.")

        st.subheader("Resultado del análisis")
        st.text_area("Reporte generado por el agente supervisor", final_report, height=420)

        st.subheader("Reglas activadas")
        for regla in inference_result["reglas_activadas"]:
            st.write(f"- {regla}")

        st.subheader("Decisiones tomadas")
        for decision in inference_result["decisiones"]:
            st.write(f"- {decision}")

elif menu == "Productos registrados":
    st.header("Productos registrados en la base de datos")

    productos = get_products()

    if productos:
        st.table(
            [
                {
                    "Producto": producto[0],
                    "Código RFID": producto[1],
                    "Precio": producto[2],
                    "Categoría": producto[3]
                }
                for producto in productos
            ]
        )
    else:
        st.warning("No hay productos registrados.")

elif menu == "Historial de eventos":
    st.header("Historial de eventos analizados")

    eventos = get_events()

    if eventos:
        for evento in eventos:
            carrito_id, producto, registrado, pago, zona, bateria, decision, explicacion = evento

            with st.expander(f"Carrito {carrito_id} - {decision}"):
                st.write(f"**Producto detectado:** {producto}")
                st.write(f"**Producto registrado:** {'Sí' if registrado else 'No'}")
                st.write(f"**Pago completado:** {'Sí' if pago else 'No'}")
                st.write(f"**Zona:** {zona}")
                st.write(f"**Batería:** {bateria}%")
                st.write(f"**Decisión:** {decision}")
                st.write(f"**Explicación:** {explicacion}")
    else:
        st.info("Todavía no hay eventos registrados.")

elif menu == "Acerca del sistema":
    st.header("Acerca de Smart-Guard Expert")

    st.write("""
Smart-Guard Expert es un prototipo de sistema experto multiagente orientado al análisis de eventos
dentro de un carrito inteligente.

El sistema forma parte de la idea general del Smart-Guard Cart, un carrito inteligente diseñado para
mejorar la seguridad, el control de productos y la experiencia de compra en tiendas o supermercados.
""")

    st.subheader("Agentes implementados")

    st.write("""
1. **Agente de Monitoreo del Carrito**  
   Recibe los datos del evento, como producto detectado, estado del pago, zona y batería.

2. **Agente de Inferencia y Seguridad**  
   Evalúa las condiciones usando reglas de inferencia.

3. **Agente Supervisor / Explicador**  
   Genera una explicación clara de las decisiones tomadas por el sistema.
""")

    st.subheader("Reglas iniciales")

    st.write("""
- Si se detecta un producto no registrado, se genera una alerta.
- Si el carrito está en salida y no tiene pago completado, se bloquea temporalmente.
- Si la batería es menor al 20%, se recomienda cargar el carrito.
- Si el producto está registrado y el pago está completo, se permite operación normal.
- Si no hay lectura RFID, se solicita nueva lectura del sensor.
""")