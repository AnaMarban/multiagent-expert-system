import streamlit as st
import pandas as pd
from datetime import datetime


st.set_page_config(
    page_title="Smart-Guard Support Center",
    page_icon="🛒",
    layout="wide"
)

# ---------------------------------------------------------
# DATOS TEMPORALES
# Estos datos solo sirven para simular cómo se verá la plataforma.
# ---------------------------------------------------------

tickets_demo = [
    {
        "ticket_id": "SGC-TK-001",
        "carrito": "SGC-004",
        "problema": "No detecta productos RFID",
        "prioridad": "Alta",
        "estado": "Abierto",
        "fecha": "2026-06-13 09:30"
    },
    {
        "ticket_id": "SGC-TK-002",
        "carrito": "SGC-002",
        "problema": "Batería baja aunque está en bahía",
        "prioridad": "Media",
        "estado": "En revisión",
        "fecha": "2026-06-13 10:15"
    },
    {
        "ticket_id": "SGC-TK-003",
        "carrito": "SGC-007",
        "problema": "No permite finalizar la compra",
        "prioridad": "Crítica",
        "estado": "Abierto",
        "fecha": "2026-06-13 11:40"
    }
]

casos_prueba = [
    "El carrito SGC-004 no detecta productos RFID.",
    "El carrito SGC-002 tiene batería baja aunque está en la bahía.",
    "El carrito SGC-007 no permite finalizar la compra.",
    "El total del carrito no coincide con los productos físicos.",
    "La pantalla del carrito SGC-003 no responde."
]

# ---------------------------------------------------------
# ESTILOS RÚSTICOS PERO CON IDENTIDAD VISUAL
# ---------------------------------------------------------

st.markdown("""
<style>
    .main-title {
        background: linear-gradient(135deg, #1e1b4b, #4338ca);
        padding: 30px;
        border-radius: 15px;
        color: white;
        margin-bottom: 25px;
    }

    .main-title h1 {
        margin: 0;
        font-size: 32px;
    }

    .main-title p {
        margin-top: 8px;
        font-size: 16px;
        opacity: 0.9;
    }

    .card {
        background: white;
        padding: 22px;
        border-radius: 12px;
        border: 1px solid #e5e7eb;
        box-shadow: 0px 2px 8px rgba(0,0,0,0.05);
        margin-bottom: 18px;
    }

    .metric-box {
        background: #f8fafc;
        padding: 20px;
        border-radius: 12px;
        border-left: 5px solid #4338ca;
    }

    .metric-number {
        font-size: 30px;
        font-weight: bold;
        color: #1e1b4b;
    }

    .metric-label {
        color: #6b7280;
        font-size: 14px;
    }

    .tag {
        display: inline-block;
        background: #e0e7ff;
        color: #3730a3;
        padding: 5px 10px;
        border-radius: 20px;
        font-size: 13px;
        font-weight: 600;
        margin-right: 5px;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------

st.sidebar.title("🛒 Smart-Guard")
st.sidebar.caption("Support Center - Versión Día 1")

menu = st.sidebar.radio(
    "Navegación",
    [
        "Panel Principal",
        "Nuevo Reporte",
        "Historial de Tickets",
        "Base de Conocimiento",
        "Sobre el Sistema"
    ]
)

st.sidebar.divider()

st.sidebar.subheader("Estado inicial")
st.sidebar.write("Tickets abiertos: 2")
st.sidebar.write("Incidencias críticas: 1")
st.sidebar.write("Carritos registrados: 7")

st.sidebar.divider()
st.sidebar.caption("Proyecto escolar - Sistema Experto")

# ---------------------------------------------------------
# PANEL PRINCIPAL
# ---------------------------------------------------------

if menu == "Panel Principal":

    st.markdown("""
    <div class="main-title">
        <h1>Smart-Guard Support Center</h1>
        <p>Plataforma inicial para registrar, revisar y diagnosticar fallas del Smart-Guard Cart.</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("""
        <div class="metric-box">
            <div class="metric-number">3</div>
            <div class="metric-label">Tickets totales</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="metric-box">
            <div class="metric-number">2</div>
            <div class="metric-label">Tickets abiertos</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="metric-box">
            <div class="metric-number">1</div>
            <div class="metric-label">Incidencias críticas</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown("""
        <div class="metric-box">
            <div class="metric-number">7</div>
            <div class="metric-label">Carritos registrados</div>
        </div>
        """, unsafe_allow_html=True)

    st.write("")

    col_a, col_b = st.columns([2, 1])

    with col_a:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Últimos tickets registrados")
        df = pd.DataFrame(tickets_demo)
        st.dataframe(df, use_container_width=True, hide_index=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_b:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Componentes más reportados")
        st.write("RFID")
        st.progress(80)
        st.write("Batería")
        st.progress(55)
        st.write("Pantalla")
        st.progress(35)
        st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# NUEVO REPORTE
# ---------------------------------------------------------

elif menu == "Nuevo Reporte":

    st.markdown("""
    <div class="main-title">
        <h1>Registrar Nuevo Reporte</h1>
        <p>Formulario básico para capturar una falla reportada por el usuario.</p>
    </div>
    """, unsafe_allow_html=True)

    col_form, col_help = st.columns([2, 1])

    with col_form:
        st.markdown('<div class="card">', unsafe_allow_html=True)

        st.subheader("Datos del reporte")

        cliente = st.selectbox(
            "Supermercado / Cliente",
            ["Supermercado Central", "Sucursal Norte", "Sucursal Sur"]
        )

        carrito = st.selectbox(
            "ID del carrito",
            [
                "No especificado",
                "SGC-001",
                "SGC-002",
                "SGC-003",
                "SGC-004",
                "SGC-005",
                "SGC-006",
                "SGC-007"
            ]
        )

        problema = st.text_area(
            "Descripción del problema",
            placeholder="Ejemplo: El carrito SGC-004 no detecta productos RFID.",
            height=130
        )

        prioridad_manual = st.selectbox(
            "Prioridad estimada",
            ["Baja", "Media", "Alta", "Crítica"]
        )

        if st.button("Generar reporte inicial"):
            if problema.strip() == "":
                st.warning("Primero escribe la descripción del problema.")
            else:
                ticket_generado = "SGC-TK-" + datetime.now().strftime("%H%M%S")

                st.success("Reporte generado correctamente.")

                st.markdown("### Resultado preliminar")
                st.write(f"**Ticket:** {ticket_generado}")
                st.write(f"**Cliente:** {cliente}")
                st.write(f"**Carrito:** {carrito}")
                st.write(f"**Prioridad:** {prioridad_manual}")
                st.write(f"**Problema reportado:** {problema}")

                st.info(
                    "En una versión posterior, este reporte será enviado al motor de inferencia "
                    "para diagnosticar automáticamente la falla."
                )

        st.markdown('</div>', unsafe_allow_html=True)

    with col_help:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Casos de prueba")

        st.caption("Estos ejemplos sirven para probar la plataforma durante el desarrollo.")

        for caso in casos_prueba:
            st.write("•", caso)

        st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# HISTORIAL DE TICKETS
# ---------------------------------------------------------

elif menu == "Historial de Tickets":

    st.markdown("""
    <div class="main-title">
        <h1>Historial de Tickets</h1>
        <p>Vista preliminar de los reportes registrados en el sistema.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.subheader("Lista de tickets")

    filtro_prioridad = st.selectbox(
        "Filtrar por prioridad",
        ["Todas", "Baja", "Media", "Alta", "Crítica"]
    )

    df = pd.DataFrame(tickets_demo)

    if filtro_prioridad != "Todas":
        df = df[df["prioridad"] == filtro_prioridad]

    st.dataframe(df, use_container_width=True, hide_index=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# BASE DE CONOCIMIENTO
# ---------------------------------------------------------

elif menu == "Base de Conocimiento":

    st.markdown("""
    <div class="main-title">
        <h1>Base de Conocimiento</h1>
        <p>Información técnica inicial del Smart-Guard Cart.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("¿Qué es Smart-Guard Cart?")

    st.write(
        "Smart-Guard Cart es un carrito inteligente diseñado para apoyar el proceso "
        "de compra dentro de un supermercado. El sistema puede identificar productos, "
        "llevar un conteo del total y apoyar al usuario durante la compra."
    )

    st.markdown("""
    <span class="tag">RFID</span>
    <span class="tag">Pantalla táctil</span>
    <span class="tag">Batería</span>
    <span class="tag">Base de carga</span>
    <span class="tag">Sistema de pago</span>
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Fallas comunes")

    fallas = {
        "RFID no detecta productos": "Puede deberse a lector dañado, etiqueta mal colocada o interferencia.",
        "Batería baja": "Puede deberse a falla en la bahía de carga o desgaste de batería.",
        "Pantalla congelada": "Puede deberse a error del sistema o falta de respuesta táctil.",
        "Total incorrecto": "Puede deberse a lectura duplicada o producto no registrado.",
        "No finaliza compra": "Puede deberse a error de conexión o fallo en el módulo de pago."
    }

    for falla, descripcion in fallas.items():
        st.write(f"**{falla}:** {descripcion}")

    st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# SOBRE EL SISTEMA
# ---------------------------------------------------------

elif menu == "Sobre el Sistema":

    st.markdown("""
    <div class="main-title">
        <h1>Sobre el Sistema</h1>
        <p>Descripción de la primera versión de desarrollo.</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Objetivo")

        st.write(
            "El objetivo de esta plataforma es permitir que un usuario registre fallas "
            "relacionadas con el Smart-Guard Cart y que el sistema pueda analizarlas "
            "mediante reglas de inferencia."
        )

        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Estado actual del avance")

        st.write("Versión inicial del proyecto.")
        st.write("La interfaz ya tiene navegación.")
        st.write("Los datos todavía son simulados.")
        st.write("Aún no existe base de datos.")
        st.write("Aún no existe motor de inferencia real.")

        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.subheader("Próximos pasos")

    st.write("1. Crear una base de datos SQLite.")
    st.write("2. Guardar los tickets reales.")
    st.write("3. Crear reglas IF/THEN.")
    st.write("4. Crear un motor de inferencia.")
    st.write("5. Separar el proyecto en carpetas y módulos.")
    st.write("6. Mejorar la explicación del diagnóstico.")

    st.markdown('</div>', unsafe_allow_html=True)