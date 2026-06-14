"""
Smart-Guard Support Center — Interfaz Principal (Streamlit)
Sistema Experto de Soporte Técnico paraSmart-Guard Cart
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
import pandas as pd
from datetime import datetime

# Inicializar BD antes de importar servicios
import database
database.init_database()

from agents import customer_agent, diagnostic_agent, supervisor_agent
from services import report_service
from base.base_conocimiento import get_all_rules

# 
# CONFIGURACIÓN DE PÁGINA
# 
st.set_page_config(
    page_title="Smart-Guard Support Center",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 
# ESTILOS CSS PERSONALIZADOS
# 
st.markdown("""
<style>
    /* Fuentes y base */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Fondo general */
    .stApp {
        background: linear-gradient(135deg, #f0f4ff 0%, #faf5ff 50%, #f0faf5 100%);
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e1b4b 0%, #312e81 60%, #4338ca 100%);
        color: white;
    }
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    [data-testid="stSidebar"] .stSelectbox label,
    [data-testid="stSidebar"] .stTextArea label {
        color: #c7d2fe !important;
        font-weight: 500;
    }

    /* Tarjetas de métricas */
    .metric-card {
        background: white;
        border-radius: 16px;
        padding: 20px 24px;
        box-shadow: 0 4px 20px rgba(99,102,241,0.08);
        border-left: 4px solid #6366f1;
        transition: transform 0.2s ease;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 30px rgba(99,102,241,0.15);
    }
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #1e1b4b;
        line-height: 1.1;
    }
    .metric-label {
        font-size: 0.8rem;
        color: #6b7280;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-top: 4px;
    }
    .metric-card.orange { border-left-color: #f59e0b; }
    .metric-card.red    { border-left-color: #ef4444; }
    .metric-card.green  { border-left-color: #10b981; }

    /* Secciones y tarjetas de contenido */
    .section-card {
        background: white;
        border-radius: 16px;
        padding: 24px 28px;
        box-shadow: 0 2px 16px rgba(0,0,0,0.06);
        margin-bottom: 20px;
        border: 1px solid #e0e7ff;
    }
    .section-title {
        font-size: 1.1rem;
        font-weight: 700;
        color: #1e1b4b;
        margin-bottom: 12px;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    /* Badge de agente */
    .agent-badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 0.03em;
    }
    .badge-blue   { background: #e0e7ff; color: #3730a3; }
    .badge-purple { background: #f3e8ff; color: #7c3aed; }
    .badge-green  { background: #dcfce7; color: #15803d; }

    /* Priority badges */
    .priority-critica { background: #fee2e2; color: #dc2626; padding: 4px 12px; border-radius: 20px; font-weight: 600; font-size: 0.8rem; }
    .priority-alta    { background: #fef3c7; color: #d97706; padding: 4px 12px; border-radius: 20px; font-weight: 600; font-size: 0.8rem; }
    .priority-media   { background: #fef9c3; color: #ca8a04; padding: 4px 12px; border-radius: 20px; font-weight: 600; font-size: 0.8rem; }
    .priority-baja    { background: #dcfce7; color: #16a34a; padding: 4px 12px; border-radius: 20px; font-weight: 600; font-size: 0.8rem; }

    /* Ticket card */
    .ticket-card {
        background: linear-gradient(135deg, #e0e7ff 0%, #f3e8ff 100%);
        border-radius: 16px;
        padding: 20px 24px;
        border: 1px solid #c7d2fe;
    }
    .ticket-id {
        font-size: 1.4rem;
        font-weight: 700;
        color: #3730a3;
        letter-spacing: 0.02em;
    }

    /* Hero header */
    .hero-header {
        background: linear-gradient(135deg, #1e1b4b 0%, #4338ca 60%, #7c3aed 100%);
        color: white;
        padding: 32px 40px;
        border-radius: 20px;
        margin-bottom: 28px;
        box-shadow: 0 8px 40px rgba(67,56,202,0.3);
    }
    .hero-title {
        font-size: 2rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        margin: 0;
    }
    .hero-sub {
        font-size: 1rem;
        opacity: 0.8;
        margin-top: 6px;
    }

    /* Reasoning steps */
    .reasoning-step {
        background: #f8fafc;
        border-radius: 10px;
        padding: 12px 16px;
        margin: 8px 0;
        border-left: 3px solid #6366f1;
        font-size: 0.9rem;
        color: #374151;
    }

    /* Rule pill */
    .rule-pill {
        display: inline-block;
        background: #e0e7ff;
        color: #3730a3;
        border-radius: 8px;
        padding: 4px 10px;
        font-size: 0.78rem;
        font-weight: 600;
        margin: 3px;
    }

    /* Divider */
    .soft-divider {
        height: 1px;
        background: linear-gradient(to right, #e0e7ff, transparent);
        margin: 20px 0;
    }

    /* Hide Streamlit branding */
    #MainMenu, footer { visibility: hidden; }
    .stDeployButton { display: none; }

    /* Test case buttons */
    .stButton > button {
        background: linear-gradient(135deg, #6366f1, #8b5cf6);
        color: white;
        border: none;
        border-radius: 10px;
        font-weight: 600;
        padding: 8px 20px;
        transition: all 0.2s ease;
        width: 100%;
    }
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 15px rgba(99,102,241,0.4);
    }
    .stButton > button[kind="secondary"] {
        background: white;
        color: #6366f1;
        border: 2px solid #6366f1;
    }

    /* Dataframe */
    .dataframe-container {
        border-radius: 12px;
        overflow: hidden;
    }
</style>
""", unsafe_allow_html=True)

# 
# CASOS DE PRUEBA PREDEFINIDOS
# 
TEST_CASES = [
    "El carrito SGC-004 no detecta productos RFID.",
    "El carrito SGC-002 tiene batería baja aunque está en la bahía.",
    "El carrito SGC-007 no permite finalizar la compra.",
    "El total del carrito no coincide con los productos físicos.",
    "La pantalla del carrito SGC-003 no responde.",
    "El lector RFID detecta el mismo producto varias veces.",
    "El carrito SGC-001 no permite iniciar sesión.",
    "El producto escaneado no existe en la base de datos.",
    "El dock magnético no está cargando el carrito.",
    "Tres carritos del supermercado presentan falla de RFID al mismo tiempo.",
]

# 
# SIDEBAR
# 
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding: 16px 0 24px 0;">
        <div style="font-size:2.5rem;"></div>
        <div style="font-size:1.1rem; font-weight:700; color:white;">Smart-Guard</div>
        <div style="font-size:0.75rem; color:#a5b4fc;">Support Center v1.0</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("<p style='font-size:0.8rem;color:#a5b4fc;font-weight:600;text-transform:uppercase;letter-spacing:0.05em;'>NAVEGACIÓN</p>", unsafe_allow_html=True)

    menu = st.radio(
        "Sección",
        ["Panel Principal", "Nuevo Reporte", "Historial de Tickets",
         "Base de Conocimiento", "Reglas del Sistema", "Sobre el Sistema"],
        label_visibility="collapsed",
    )

    st.markdown("---")

    # Métricas rápidas en sidebar
    metrics = report_service.get_dashboard_metrics()
    st.markdown(f"""
    <div style="background:rgba(255,255,255,0.1);border-radius:12px;padding:14px;">
        <div style="font-size:0.7rem;color:#a5b4fc;font-weight:600;text-transform:uppercase;letter-spacing:0.05em;margin-bottom:10px;">Estado del Sistema</div>
        <div style="display:flex;justify-content:space-between;margin-bottom:8px;">
            <span style="color:#c7d2fe;font-size:0.85rem;">Tickets abiertos</span>
            <span style="color:white;font-weight:700;">{metrics['open_tickets']}</span>
        </div>
        <div style="display:flex;justify-content:space-between;margin-bottom:8px;">
            <span style="color:#c7d2fe;font-size:0.85rem;">Incidencias críticas</span>
            <span style="color:#fca5a5;font-weight:700;">{metrics['critical_tickets']}</span>
        </div>
        <div style="display:flex;justify-content:space-between;">
            <span style="color:#c7d2fe;font-size:0.85rem;">Carritos registrados</span>
            <span style="color:white;font-weight:700;">{metrics['total_carts']}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("<p style='font-size:0.7rem;color:#6366f1;text-align:center;'>Sistema Experto Local · SQLite · Python</p>", unsafe_allow_html=True)


# 
# PANEL PRINCIPAL
# 
if "Panel Principal" in menu:
    # Hero
    st.markdown("""
    <div class="hero-header">
        <p class="hero-title">Smart-Guard Support Center</p>
        <p class="hero-sub">Sistema Experto de Soporte Técnico paraSmart-Guard Cart</p>
    </div>
    """, unsafe_allow_html=True)

    # Métricas
    metrics = report_service.get_dashboard_metrics()
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{metrics['open_tickets']}</div>
            <div class="metric-label"> Tickets Abiertos</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="metric-card orange">
            <div class="metric-value">{metrics['total_carts']}</div>
            <div class="metric-label"> Carritos Registrados</div>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
        <div class="metric-card red">
            <div class="metric-value">{metrics['critical_tickets']}</div>
            <div class="metric-label"> Incidencias Críticas</div>
        </div>""", unsafe_allow_html=True)
    with c4:
        st.markdown(f"""
        <div class="metric-card green">
            <div class="metric-value" style="font-size:1.3rem;">{metrics['estimated_time']}</div>
            <div class="metric-label">⏱ Tiempo Est. Atención</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col_a, col_b = st.columns([3, 2])

    with col_a:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title"> Últimos Tickets</div>', unsafe_allow_html=True)
        recent = report_service.get_tickets_history(limit=8)
        if recent:
            rows = []
            for t in recent:
                priority = t.get("priority", "baja")
                emoji = {"critica": "", "alta": "", "media": "", "baja": ""}.get(priority, "")
                rows.append({
                    "Ticket": t["ticket_id"],
                    "Carrito": t.get("cart_id", "N/A"),
                    "Categoría": t.get("category", ""),
                    "Prioridad": f"{emoji} {priority.capitalize()}",
                    "Estado": t.get("status", ""),
                    "Fecha": t.get("created_at", "")[:16],
                })
            df = pd.DataFrame(rows)
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("No hay tickets registrados aún. ¡Registra el primero!")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_b:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title"> Carritos con Más Incidencias</div>', unsafe_allow_html=True)
        affected = report_service.get_most_affected_carts()
        if affected:
            for a in affected:
                pct = min(a["total"] * 20, 100)
                st.markdown(f"""
                <div style="margin-bottom:12px;">
                    <div style="display:flex;justify-content:space-between;margin-bottom:4px;">
                        <span style="font-weight:600;color:#374151;">{a['cart_id']}</span>
                        <span style="color:#6b7280;font-size:0.85rem;">{a['total']} ticket(s)</span>
                    </div>
                    <div style="background:#e0e7ff;border-radius:4px;height:6px;">
                        <div style="background:linear-gradient(to right,#6366f1,#8b5cf6);
                                    width:{pct}%;height:6px;border-radius:4px;"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Sin datos de incidencias aún.")

        st.markdown("<div class='soft-divider'></div>", unsafe_allow_html=True)
        st.markdown('<div class="section-title"> Estadísticas</div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;">
            <div style="background:#f0fdf4;border-radius:10px;padding:14px;text-align:center;">
                <div style="font-size:1.6rem;font-weight:700;color:#15803d;">{metrics['resolved_tickets']}</div>
                <div style="font-size:0.75rem;color:#6b7280;">Resueltos</div>
            </div>
            <div style="background:#f0f4ff;border-radius:10px;padding:14px;text-align:center;">
                <div style="font-size:1.6rem;font-weight:700;color:#4338ca;">{metrics['total_tickets']}</div>
                <div style="font-size:0.75rem;color:#6b7280;">Total</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# 
# NUEVO REPORTE
# 
elif "Nuevo Reporte" in menu:
    st.markdown("""
    <div class="hero-header">
        <p class="hero-title">Registrar Nuevo Reporte</p>
        <p class="hero-sub">Describe el problema y los 3 agentes del sistema experto lo analizarán</p>
    </div>
    """, unsafe_allow_html=True)

    col_form, col_cases = st.columns([3, 2])

    with col_form:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Formulario de Reporte</div>', unsafe_allow_html=True)

        clients = database.get_clients()
        client_options = {c["name"]: c["id"] for c in clients}
        selected_client_name = st.selectbox(" Supermercado", list(client_options.keys()))
        selected_client_id = client_options[selected_client_name]

        carts = database.get_carts(selected_client_id)
        cart_options = ["No especificado"] + [c["cart_id"] for c in carts]
        selected_cart = st.selectbox(" ID del Carrito (opcional)", cart_options)

        report_text = st.text_area(
            " Describe el problema",
            height=120,
            placeholder="Ej: El carrito SGC-004 no detecta productos RFID al pasar por el lector...",
            key="report_text_area",
        )

        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            analyze_btn = st.button(" Analizar Reporte", use_container_width=True)
        with col_btn2:
            clear_btn = st.button(" Limpiar", use_container_width=True)

        if clear_btn:
            st.session_state["report_text_area"] = ""
            st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

    with col_cases:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Casos de Prueba</div>', unsafe_allow_html=True)
        st.markdown("<p style='font-size:0.85rem;color:#6b7280;margin-bottom:12px;'>Haz clic en cualquier caso para cargarlo automáticamente:</p>", unsafe_allow_html=True)
        for i, case in enumerate(TEST_CASES):
            if st.button(f"#{i+1} {case[:45]}...", key=f"case_{i}"):
                st.session_state["loaded_case"] = case
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # Cargar caso de prueba si se seleccionó
    if "loaded_case" in st.session_state:
        report_text = st.session_state["loaded_case"]
        st.info(f" Caso cargado: *{report_text}*")

    #  PROCESAMIENTO DE LOS 3 AGENTES 
    if analyze_btn and report_text:
        if selected_cart != "No especificado" and selected_cart not in report_text:
            report_text = report_text + f" (Carrito: {selected_cart})"

        with st.spinner(" Ejecutando agentes del sistema experto..."):
            # AGENTE 1
            a1_result = customer_agent.process(report_text, client_id=selected_client_id)

            # AGENTE 2
            a2_result = diagnostic_agent.process(a1_result, client_id=selected_client_id)

            # AGENTE 3
            a3_result = supervisor_agent.process(a1_result, a2_result)

        st.success(" Análisis completado por los 3 agentes")
        st.markdown("<br>", unsafe_allow_html=True)

        #  RESULTADO AGENTE 1 
        st.markdown("""
        <div class="section-card" style="border-left: 4px solid #6366f1;">
            <div class="section-title">
                 Agente 1 — Atencion al Cliente
                <span class="agent-badge badge-blue">Interprete</span>
            </div>
        """, unsafe_allow_html=True)

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Intención", a1_result["intent"].replace("_", " ").title())
        c2.metric("Componente", a1_result["component"])
        c3.metric("Urgencia", a1_result["urgency"].title())
        c4.metric("Carrito", a1_result["cart_id"] or "N/A")

        st.markdown(f"""
        <div style="background:#f0f4ff;border-radius:10px;padding:14px;margin-top:12px;">
            <b>Categoría:</b> {a1_result['category']}<br>
            <b>Palabras clave:</b> {', '.join(a1_result['keywords']) if a1_result['keywords'] else 'N/A'}<br>
            <b>Nota:</b> {a1_result['notes']}
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        #  RESULTADO AGENTE 2 
        priority = a2_result["priority"]
        priority_colors = {"critica": "#fee2e2", "alta": "#fef3c7", "media": "#fef9c3", "baja": "#dcfce7"}
        priority_emojis = {"critica": "", "alta": "", "media": "", "baja": ""}
        bg_color = priority_colors.get(priority, "#f0f4ff")
        p_emoji = priority_emojis.get(priority, "")

        st.markdown(f"""
        <div class="section-card" style="border-left: 4px solid #7c3aed;">
            <div class="section-title">
                 Agente 2 — Diagnostico y Ticket
                <span class="agent-badge badge-purple">Diagnostico</span>
            </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="ticket-card" style="margin-bottom:16px;">
            <div class="ticket-id">{a2_result['ticket_id']}</div>
            <div style="font-size:0.8rem;color:#6366f1;margin-top:4px;">Ticket generado exitosamente</div>
        </div>
        """, unsafe_allow_html=True)

        d1, d2, d3 = st.columns(3)
        d1.metric("Diagnóstico", a2_result["diagnosis"])
        d2.metric("Prioridad", f"{p_emoji} {priority.title()}")
        d3.metric("Confianza", f"{a2_result['confidence']:.0%}")

        st.markdown(f"""
        <div style="background:{bg_color};border-radius:10px;padding:14px;margin-top:12px;">
            <b> Solución Recomendada:</b><br>
            {a2_result['recommendation']}
        </div>
        """, unsafe_allow_html=True)

        # Reglas aplicadas
        rules_html = "".join([f'<span class="rule-pill">{r}</span>' for r in a2_result["rules_applied"]])
        st.markdown(f"""
        <div style="margin-top:12px;">
            <b>Reglas aplicadas:</b> {rules_html}
        </div>
        """, unsafe_allow_html=True)

        if a2_result["previous_tickets"] > 0:
            st.warning(f" Este carrito tiene {a2_result['previous_tickets']} incidencia(s) previas.")

        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        #  RESULTADO AGENTE 3 
        st.markdown("""
        <div class="section-card" style="border-left: 4px solid #10b981;">
            <div class="section-title">
                 Agente 3 — Supervisor / Explicador
                <span class="agent-badge badge-green">Explicabilidad</span>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("** Resumen del Sistema Experto:**")
        st.markdown(a3_result["summary"])

        st.markdown("<div class='soft-divider'></div>", unsafe_allow_html=True)
        st.markdown("** Razonamiento Paso a Paso:**")
        for step in a3_result["reasoning_steps"]:
            st.markdown(f'<div class="reasoning-step">{step}</div>', unsafe_allow_html=True)

        if a3_result["all_explanations"]:
            st.markdown("<div class='soft-divider'></div>", unsafe_allow_html=True)
            st.markdown("** Detalle de Reglas Activadas:**")
            for exp in a3_result["all_explanations"]:
                st.markdown(f'<div class="reasoning-step">{exp}</div>', unsafe_allow_html=True)

        st.markdown(f"""
        <div style="background:#f0fdf4;border-radius:10px;padding:14px;margin-top:16px;border:1px solid #bbf7d0;">
            {a3_result['validation_message']}
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # Guardar en session_state para consulta posterior
        st.session_state["last_analysis"] = {
            "a1": a1_result, "a2": a2_result, "a3": a3_result
        }

    elif analyze_btn and not report_text:
        st.warning(" Por favor, escribe un reporte o selecciona un caso de prueba.")

    # Mostrar caso cargado si no se ha analizado aún
    if "loaded_case" in st.session_state and not analyze_btn:
        st.markdown(f"""
        <div class="section-card">
            <div class="section-title"> Caso de Prueba Cargado</div>
            <p style="color:#374151;">{st.session_state['loaded_case']}</p>
            <p style="color:#6b7280;font-size:0.85rem;">Presiona "Analizar Reporte" para procesar este caso.</p>
        </div>
        """, unsafe_allow_html=True)

# 
# HISTORIAL DE TICKETS
# 
elif "Historial de Tickets" in menu:
    st.markdown("""
    <div class="hero-header">
        <p class="hero-title">Historial de Tickets</p>
        <p class="hero-sub">Registro completo de incidencias y diagnósticos</p>
    </div>
    """, unsafe_allow_html=True)

    tickets = report_service.get_tickets_history(limit=50)
    if tickets:
        # Filtros
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            filter_priority = st.selectbox(
                "Filtrar por prioridad",
                ["Todas", "critica", "alta", "media", "baja"],
            )
        with col_f2:
            filter_status = st.selectbox(
                "Filtrar por estado",
                ["Todos", "abierto", "en_proceso", "resuelto", "cerrado"],
            )

        rows = []
        for t in tickets:
            if filter_priority != "Todas" and t.get("priority") != filter_priority:
                continue
            if filter_status != "Todos" and t.get("status") != filter_status:
                continue
            p = t.get("priority", "baja")
            emoji = {"critica": "", "alta": "", "media": "", "baja": ""}.get(p, "")
            rows.append({
                " Ticket ID":  t["ticket_id"],
                " Carrito":    t.get("cart_id", "N/A"),
                " Cliente":    t.get("client_name", "N/A"),
                " Categoría":  t.get("category", ""),
                " Diagnóstico":t.get("diagnosis", "")[:40] + "..." if t.get("diagnosis", "") and len(t.get("diagnosis", "")) > 40 else t.get("diagnosis", ""),
                " Prioridad":  f"{emoji} {p.capitalize()}",
                " Estado":     t.get("status", ""),
                " Fecha":      t.get("created_at", "")[:16],
            })

        if rows:
            df = pd.DataFrame(rows)
            st.dataframe(df, use_container_width=True, hide_index=True)
            st.markdown(f"<p style='color:#6b7280;font-size:0.85rem;text-align:right;'>Mostrando {len(rows)} ticket(s)</p>", unsafe_allow_html=True)
        else:
            st.info("No hay tickets que coincidan con los filtros seleccionados.")
    else:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.info(" No hay tickets registrados. Ve a **Nuevo Reporte** para crear el primero.")
        st.markdown('</div>', unsafe_allow_html=True)

# 
# BASE DE CONOCIMIENTO
# 
elif "Base de Conocimiento" in menu:
    from base.support_knowledge import get_product_info, get_operation_flow

    st.markdown("""
    <div class="hero-header">
        <p class="hero-title">Base de Conocimiento</p>
        <p class="hero-sub">Información técnica delSmart-Guard Cart</p>
    </div>
    """, unsafe_allow_html=True)

    info = get_product_info()

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="section-title"> {info['name']}</div>
    <p style="color:#374151;">{info['description']}</p>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Componentes
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Componentes Principales</div>', unsafe_allow_html=True)
    cols = st.columns(3)
    for i, comp in enumerate(info["components"]):
        with cols[i % 3]:
            st.markdown(f"""
            <div style="background:#f8fafc;border-radius:10px;padding:14px;margin-bottom:12px;border:1px solid #e0e7ff;">
                <div style="font-weight:600;color:#1e1b4b;margin-bottom:4px;">{comp['name']}</div>
                <div style="font-size:0.8rem;color:#6366f1;margin-bottom:6px;">{comp['role']}</div>
                <div style="font-size:0.8rem;color:#6b7280;">{comp['details']}</div>
            </div>
            """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Flujo de operación
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title"> Flujo de Operación</div>', unsafe_allow_html=True)
    for step in get_operation_flow():
        st.markdown(f"""
        <div style="display:flex;gap:16px;margin-bottom:16px;">
            <div style="background:linear-gradient(135deg,#6366f1,#8b5cf6);color:white;border-radius:50%;
                        width:32px;height:32px;display:flex;align-items:center;justify-content:center;
                        font-weight:700;font-size:0.9rem;flex-shrink:0;">{step['step']}</div>
            <div>
                <div style="font-weight:600;color:#1e1b4b;">{step['title']}</div>
                <div style="font-size:0.85rem;color:#6b7280;margin-top:3px;">{step['description']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Fallas comunes
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Fallas Comunes</div>', unsafe_allow_html=True)
    for failure in info["common_failures"]:
        freq_color = {"Alta": "#fee2e2", "Media": "#fef3c7", "Baja": "#dcfce7"}.get(failure["frequency"], "#f0f4ff")
        st.markdown(f"""
        <div style="background:{freq_color};border-radius:10px;padding:14px;margin-bottom:10px;">
            <div style="font-weight:600;color:#1e1b4b;">{failure['failure']}
                <span style="font-size:0.75rem;color:#6b7280;margin-left:8px;">Frecuencia: {failure['frequency']}</span>
            </div>
            <div style="font-size:0.83rem;color:#374151;margin-top:4px;">
                <b>Causas:</b> {', '.join(failure['causes'])}<br>
                <b>Solución rápida:</b> {failure['quick_fix']}
            </div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# 
# REGLAS DEL SISTEMA
# 
elif "Reglas del Sistema" in menu:
    st.markdown("""
    <div class="hero-header">
        <p class="hero-title">Reglas de Inferencia</p>
        <p class="hero-sub">Base de reglas IF/THEN del sistema experto</p>
    </div>
    """, unsafe_allow_html=True)

    rules = get_all_rules()
    priority_colors = {"critica": "#fee2e2", "alta": "#fef3c7", "media": "#f0f4ff", "baja": "#dcfce7"}
    priority_border = {"critica": "#ef4444", "alta": "#f59e0b", "media": "#6366f1", "baja": "#10b981"}

    st.markdown(f"<p style='color:#6b7280;margin-bottom:20px;'>El sistema cuenta con <b>{len(rules)}</b> reglas de inferencia activas.</p>", unsafe_allow_html=True)

    for rule in rules:
        bg = priority_colors.get(rule["priority"], "#f0f4ff")
        border = priority_border.get(rule["priority"], "#6366f1")
        priority_emoji = {"critica": "", "alta": "", "media": "", "baja": ""}.get(rule["priority"], "")

        conditions_str = " | ".join(rule["conditions"][:4])

        st.markdown(f"""
        <div style="background:{bg};border-radius:12px;padding:18px 20px;margin-bottom:12px;
                    border-left:4px solid {border};">
            <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:10px;">
                <div>
                    <span style="background:{border};color:white;padding:2px 10px;border-radius:8px;
                                 font-size:0.75rem;font-weight:700;">{rule['id']}</span>
                    <span style="font-weight:700;color:#1e1b4b;margin-left:10px;">{rule['name']}</span>
                </div>
                <span>{priority_emoji} {rule['priority'].capitalize()}</span>
            </div>
            <div style="font-size:0.85rem;color:#374151;margin-bottom:8px;">
                <b>SI:</b> {conditions_str}<br>
                <b>ENTONCES:</b> {rule['result']}
            </div>
            <div style="font-size:0.83rem;color:#6b7280;">
                <b>Componente:</b> {rule['component']} &nbsp;|&nbsp;
                <b>Recomendación:</b> {rule['recommendation'][:80]}...
            </div>
        </div>
        """, unsafe_allow_html=True)

# 
# SOBRE EL SISTEMA
# 
elif "Sobre el Sistema" in menu:
    st.markdown("""
    <div class="hero-header">
        <p class="hero-title">ℹSobre el Sistema</p>
        <p class="hero-sub">Arquitectura, cumplimiento académico y descripción del proyecto</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Arquitectura del Sistema</div>', unsafe_allow_html=True)
        st.markdown("""
        ```
        Usuario (Streamlit UI)
               
               
        Agente 1: Atención al Cliente
         Detecta intención, componente, urgencia
               
               
        Motor de Inferencia (IF/THEN)
         Evalúa reglas R1-R15
               
               
        Agente 2: Diagnóstico y Ticket
         Genera ticket + guarda en SQLite
               
               
        Agente 3: Supervisor/Explicador
         Genera razonamiento explicable
               
               
        Base de Datos SQLite
        (tickets, diagnostics, inference_logs)
        ```
        """)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title"> Cumplimiento Académico</div>', unsafe_allow_html=True)
        requirements = [
            ("Sistema experto moderno", True),
            ("Ingeniería del conocimiento", True),
            ("Base de conocimiento", True),
            ("Reglas IF/THEN (15 reglas)", True),
            ("Motor de inferencia propio", True),
            ("Base de datos SQLite", True),
            ("3 agentes inteligentes", True),
            ("Explicabilidad del razonamiento", True),
            ("Interacción usuario-sistema", True),
            ("Arquitectura local funcional", True),
            ("Preparado para GitHub", True),
            ("README incluido", True),
            ("Manual de usuario", True),
            ("Instrucciones de instalación", True),
            ("Casos de prueba (10)", True),
            ("Documentación para PDF", True),
            ("100% local, sin API Key", True),
            ("Organizado en módulos", True),
        ]
        for req, ok in requirements:
            icon = "" if ok else ""
            st.markdown(f"<div style='padding:4px 0;font-size:0.85rem;'>{icon} {req}</div>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title"> Tecnologías Utilizadas</div>', unsafe_allow_html=True)
    tech_cols = st.columns(4)
    techs = [
        (" Python", "Lenguaje principal"),
        (" Streamlit", "Interfaz web local"),
        (" SQLite", "Base de datos local"),
        (" Motor IF/THEN", "Inferencia propia"),
    ]
    for i, (tech, desc) in enumerate(techs):
        with tech_cols[i]:
            st.markdown(f"""
            <div style="text-align:center;background:#f0f4ff;border-radius:10px;padding:16px;">
                <div style="font-size:1.5rem;">{tech.split()[0]}</div>
                <div style="font-weight:600;color:#1e1b4b;font-size:0.9rem;">{tech.split(' ', 1)[1]}</div>
                <div style="color:#6b7280;font-size:0.78rem;margin-top:4px;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
