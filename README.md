# Smart-Guard Support Center

Sistema experto de soporte tecnico para supermercados que usan el carrito inteligente Smart-Guard Cart.

---

## Que hace

Recibe reportes de fallas en los carritos, los interpreta con 3 agentes, aplica reglas de diagnostico y genera un ticket con prioridad y explicacion. Todo funciona local, sin internet y sin API Key.

---

## Como fue creciendo el proyecto

**28 mayo — Primer commit / README inicial**
Empezo con la idea: un sistema de soporte para el Smart-Guard Cart.
El README describe que va a ser y por que.

**29 mayo — Base de datos**
Defini las tablas que iba a necesitar: clientes, carritos, tickets, diagnosticos, logs.
Aprendi a usar SQLite porque no queria instalar MySQL para algo local.
La funcion init_database() crea todo automaticamente si no existe.

**30 mayo — Agents**
Cree los tres agentes. Cada uno en su propio archivo porque cada uno hace una cosa distinta.
El Agente 1 lee el mensaje. El Agente 2 diagnostica. El Agente 3 explica.

**01 junio — Rules / Base de conocimiento**
Defini las 15 reglas IF/THEN. Cada regla tiene condiciones, resultado, prioridad y recomendacion.
Estuve investigando que fallas son comunes en sistemas RFID y Raspberry Pi para que las reglas tuvieran sentido real.

**04 junio — Main / Interfaz inicial**
Primera version del dashboard en Streamlit. Sin CSS todavia, solo la estructura.
Descubri que Streamlit ejecuta el archivo completo cada vez que el usuario hace algo, lo cual cambio como organice el codigo.

**09 junio — Actualizacion main**
Mejore el diseno visual con CSS inyectado, agregue los casos de prueba como botones,
y conecte los 3 agentes para que se muestren en orden con colores distintos.

**13 junio — Interfaz y motor de inferencia**
Renombre archivos para que tengan mas sentido (interfaz.py, motor_inferencia.py, base_conocimiento.py).
Complete el motor de inferencia: calcula confianza para cada regla, las ordena y selecciona la mejor.
Agregue la inferencia encadenada: si el carrito tiene tickets previos, la prioridad sube automaticamente.

**14 junio — Documentacion final**
Manual de usuario, bitacora de desarrollo y explicacion del codigo por secciones.

---

## Tecnologias

- Python 3.10+
- Streamlit (interfaz web local)
- SQLite (base de datos sin servidor)
- Pandas (tablas en la UI)
- Motor de reglas propio sin dependencias externas

---

## Estructura

```
SmartGuard_SupportCenter/
  interfaz.py          <- dashboard principal
  database.py          <- gestion de SQLite
  config.py            <- constantes globales
  agents/
    customer_agent.py  <- Agente 1: interpreta el mensaje
    diagnostic_agent.py <- Agente 2: diagnostica y crea ticket
    supervisor_agent.py <- Agente 3: explica la decision
  base/
    base_conocimiento.py <- 15 reglas IF/THEN
    support_knowledge.py <- info del Smart-Guard Cart
  services/
    motor_inferencia.py  <- evalua las reglas
    ticket_service.py    <- crea y guarda tickets
    report_service.py    <- metricas y estadisticas
  data/
    smartguard_support.db (se crea automaticamente)
  docs/
    bitacora_desarrollo.md
    manual_usuario.md
    explicacion_codigo.md
```

---

## Instalacion y uso

```
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run interfaz.py
```

Abre el navegador en http://localhost:8501

---

## Casos de prueba incluidos

10 casos listos en la interfaz. Los mas utiles para demostrar:
- Caso 1: falla RFID basica
- Caso 2: bateria baja en la bahia (distingue de bateria baja fuera de bahia)
- Caso 10: tres carritos con falla al mismo tiempo (prioridad critica)
