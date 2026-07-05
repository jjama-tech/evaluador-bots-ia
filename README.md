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
---

## Instrucciones de Instalación y Ejecución
Prerrequisitos
Sistema Operativo: Windows 10/11.

Python 3.13 o superior instalado.

Ollama instalado y autenticado localmente en la PC con acceso activo a Ollama Cloud (gemma4:31b-cloud).

Pasos para la configuración local
1. Clonar el repositorio:
git clone [https://github.com/jjama-tech/evaluador-bots-ia.git]
cd simulador_clientes_ai

2. Crear y activar el entorno virtual en Windows (PowerShell):
python -m venv .venv --without-pip
.venv\Scripts\Activate.ps1
python -m ensurepip --default-pip

3. Instalar las dependencias del proyecto (limpiando caché para compatibilidad):
pip install -r requirements.txt --no-cache-dir

4. Configurar el archivo de entorno de seguridad:

Duplica o renombra el archivo .env.example con el nombre .env.

Agrega los accesos correspondientes a tu API de Ollama Cloud. (Nota: El archivo .env se encuentra protegido en el .gitignore para salvaguardar tus credenciales).

5. Iniciar la aplicación con interfaz gráfica:
streamlit run app.py

De no abrirse de forma automática, copie y pegue en su navegador web la dirección local: http://localhost:8501

## Ejemplos de Respuestas del Agente
Caso: Cliente Enojado (Región Costa) — Intermitencia de señal
Bot de Soporte Auditado: Buenas tardes, estimado cliente. ¿Me podría indicar si ya desconectó y volvió a conectar su router de internet de la toma de corriente?

Cliente Simulado (Gemma 4): ¡Vea amigo, ya le estoy diciendo que reinicié esa nota como tres veces! No me venga con amagues que de ley necesito trabajar para ganarme el pan. Ya me da iras que todas las semanas es el mismo colmo con la señal.

Caso: Cliente Preocupado (Región Sierra) — Lentitud en Teletrabajo
Bot de Soporte Auditado: Su caso ha sido registrado en nuestro sistema. Un técnico especializado se comunicará con usted en un lapso estimado de 24 a 48 horas.

Cliente Simulado (Gemma 4): Chuta, ¿24 horas? Deme una manito porfa, sea buena gente. Mire que mis hijos tienen examen virtual mañana tempranito y yo debo entregar informes de la oficina. De una necesito resolver esta lentitud, ayúdeme chequeando desde allá.

## 📐 Diseño de Arquitectura del Agente

```text
[ Panel de Control Streamlit ]  ---> (Elige Humor, Región y Caso Técnico)
             │
             ▼
[ Historial de Conversación ]  <---> [ Motor LangChain + gemma4:31b-cloud ]
             │
             ▼
[ Botón: Generar Reporte ]     ---> [ Analizador QA ] ---> (Reporte en Barra Lateral)