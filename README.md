# 🤖 Evaluador de Bots IA — Simulador de Clientes Ecuatorianos

## 📝 Descripción del Proyecto
Este proyecto es una plataforma avanzada de Aseguramiento de Calidad (QA) y auditoría automatizada diseñada para estresar y evaluar el desempeño de bots de atención al cliente. El sistema parametriza el comportamiento, región geográfica y estado de ánimo de un cliente ficticio, obligando al modelo de lenguaje a utilizar de forma natural modismos y jergas típicas del contexto ecuatoriano. 

El principal objetivo es automatizar las etapas de prueba de los agentes de soporte técnico en situaciones cotidianas de conectividad de internet, asegurando que los bots mantengan estándares altos de empatía, resolución y velocidad. Al finalizar la interacción, el simulador genera de forma autónoma un reporte estructurado con un análisis de sentimiento detallado y recomendaciones técnicas de optimización.

---

## 🛠️ Listado de Componentes y Capas (Tools del Sistema)

El agente opera bajo una arquitectura modular compuesta por tres componentes lógicos:
1. **Motor de Simulación Emocional:** Impulsado por `gemma4:31b-cloud` mediante la infraestructura de Ollama y orquestado con LangChain. Controla la memoria del canal mediante objetos de mensajería estructurada.
2. **Inyector de Identidad Local:** Filtro semántico adaptativo que selecciona modismos específicos de la Costa y de la Sierra ecuatoriana según el nivel de frustración configurado, impidiendo que el bot caiga en caricaturas o exageraciones.
3. **Auditor Experto de Calidad (QA Tool):** Módulo de análisis independiente que procesa la transcripción completa del historial al terminar la interacción para emitir las métricas de evaluación del servicio.

---

## 📐 Diseño de Arquitectura del Agente

```text
[ Panel de Control Streamlit ]  ---> (Elige Humor, Región y Caso Técnico)
             │
             ▼
[ Historial de Conversación ]  <---> [ Motor LangChain + gemma4:31b-cloud ]
             │
             ▼
[ Botón: Generar Reporte ]     ---> [ Analizador QA ] ---> (Reporte en Barra Lateral)
