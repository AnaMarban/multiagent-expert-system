# Sistema Experto Multiagente de Inferencia e IA Aplicada

Este repositorio contiene el desarrollo del proyecto final para la materia de **Sistemas Expertos**. Consiste en un sistema moderno basado en arquitectura de multiagentes inteligentes capaz de interactuar con usuarios, realizar inferencias lógicas mediante un motor de reglas y explicar su razonamiento.

##  Stack Tecnológico (Propuesto)
- **Lenguaje:** Python 3.10+
- **Framework de Agentes:** CrewAI / LangChain
- **Orquestación de Modelos:** Ollama (Local) o Gemini API / OpenRouter
- **Base de Datos:** SQLite / Supabase
- **Interfaz de Usuario:** Streamlit / Telegram Bot

---

##  Arquitectura del Sistema (Multiagentes)
El sistema está compuesto por 3 agentes principales que operan de manera local y cliente-servidor:

1. **Agente de Atención al Cliente (Front-facing):** Encargado de la interacción inicial, detección de intenciones y extracción de entidades (productos, fallas, solicitudes).
2. **Agente Generador de Pedidos/Diagnósticos (Motor de Inferencia):** Procesa la información del Agente 1, consulta la base de datos y aplica reglas de negocio/inferencia (Ej. `IF stock < cantidad THEN sugerir_reabastecimiento`).
3. **Agente Supervisor y Explicador (Auditor):** Valida las acciones de los agentes anteriores y genera un reporte en lenguaje natural explicando el porqué de las decisiones tomadas.

---

##  Plan de Desarrollo y Commits Diarios
Para garantizar el cumplimiento de la rúbrica de desarrollo continuo, el proyecto se dividirá en las siguientes fases:

- [x] **Fase 1:** Definición de arquitectura, alcance del proyecto y estructura del repositorio.
- [ ] **Fase 2:** Configuración del entorno virtual, base de datos inicial y modelos locales/APIs.
- [ ] **Fase 3:** Desarrollo e integración del Agente 1 (Atención) y Agente 2 (Inferencia).
- [ ] **Fase 4:** Implementación del Agente 3 (Explicabilidad) y lógica de comunicación inter-agente.
- [ ] **Fase 5:** Desarrollo de la interfaz de usuario, pruebas de integración y manual de usuario.
- [ ] **Fase 6:** Documentación final (PDF), grabación del video demostrativo y despliegue local.

---
## 📄 Entregables Incluidos
* `/docs/GG_registro_Proy.pdf` (Documento final, Manual de Usuario y enlace a YouTube)
* `/src` (Código fuente del sistema)