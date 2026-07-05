import os
from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage

# 1. Cargar variables de entorno desde el archivo .env seguro
load_dotenv()

def inicializar_modelo():
    """Inicializa el modelo Gemma 4 usando las variables del archivo .env como respaldo."""
    # Intentamos leer las credenciales del archivo .env
    base_url = os.getenv("OLLAMA_API_URL")
    
    # Si las variables existen en el .env, las usamos explícitamente
    if base_url:
        return ChatOllama(
            model="gemma4:31b-cloud",
            base_url=base_url, # Usa la URL de tu .env
            temperature=0.7
        )
    else:
        # Si no existen, cae en el comportamiento por defecto (tu sesión local de la PC)
        return ChatOllama(
            model="gemma4:31b-cloud",
            temperature=0.7
        )

def generar_system_prompt(humor: str, region: str, caso_tecnico: str) -> str:
    """Construye dinámicamente las instrucciones de personalidad del cliente ficticio."""
    
    # Definición de jergas base para guiar al modelo según la región y humor
    jergas = ""
    if humor.lower() in ["enojado", "frustrado"]:
        jergas = "- Usa quejas como: 'estoy hecho una fiera','le dieron un machetazo a la fibra', 'es el colmo', 'me están amagando / puro amague', 'ya me da iras', 'pura labia', 'siempre es lo mismo','para cobrar son buenos'."
    elif humor.lower() == "preocupado":
        jergas = "- Usa expresiones como: 'chuta', 'deme una manito porfa', 'de ley necesito', 'estoy en apuros', 'solo unos diitas mas','mañana si pago','aquisito no mas','a que vas vos ves' ."
    else: # Feliz o Amable
        jergas = "- Usa expresiones como: '¡qué chevere!', 'de una', 'bacán', 'así si da gusto', 'ya posi', 'bello bello'."

    prompt = f"""Eres un ciudadano ecuatoriano real que está chateando con un bot de soporte técnico y atencion al cliente de su proveedor de internet. 
Tu único objetivo es actuar estrictamente bajo los siguientes parámetros de simulación y NO salirte del personaje bajo ningún concepto.

[PARÁMETROS DE TU PERSONALIDAD]
- Tu estado de ánimo actual es: {humor}
- Tu ubicación/región en Ecuador es: {region}
- El problema técnico ficticio que estás experimentando es: {caso_tecnico}

[REGLAS DE COMPORTAMIENTO MANDATORIAS]
1. Adopta el humor asignado de forma realista. Si estás ENOJADO, sé tajante, exige soluciones inmediatas y quéjate si te piden reiniciar el módem por quinta vez.
2. Manejo de Jerga Ecuatoriana: Incorpora de forma natural las siguientes expresiones según tu estado de ánimo:
   {jergas}
   *Nota: Usa máximo una o dos expresiones locales por mensaje para que suene humano y no parezca una caricatura.*
3. NUNCA menciones nombres de marcas comerciales reales de internet en Ecuador. Si debes referirte a tu empresa proveedora, llámala "JJ Network" o "MiProveedor".
4. Escribe respuestas de longitud humana para un chat (frases de 1 a 3 líneas). No generes textos gigantescos.
5. Responde SIEMPRE en español, adaptando sutilmente el acento según la región si es posible (Sierra/Costa).
"""
    return prompt

def simular_respuesta_cliente(humor: str, region: str, caso_tecnico: str, historial_conversacion: list) -> str:
    """
    Recibe los parámetros de configuración y el historial de chat de la interfaz,
    invoca a Gemma 4 y devuelve la siguiente frase simulada del cliente.
    """
    llm = inicializar_modelo()
    system_instruction = generar_system_prompt(humor, region, caso_tecnico)
    
    # Creamos la estructura del prompt combinando las instrucciones del sistema y el historial
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", system_instruction),
        MessagesPlaceholder(variable_name="chat_history"),
    ])
    
    # Convertimos el historial plano de la interfaz a objetos de mensaje que LangChain entiende
    # (Suponiendo que el historial viene como una lista de tuplas: [("bot", "Hola"), ("cliente", "Buenas")])
    langchain_messages = []
    for rol, texto in historial_conversacion:
        if rol == "cliente":
            langchain_messages.append(AIMessage(content=texto)) # Para nuestro LLM, el cliente es el AI
        else:
            langchain_messages.append(HumanMessage(content=texto)) # El bot de soporte externo actúa como el humano que le habla
            
    # Unimos el prompt y el modelo usando la sintaxis LCEL de LangChain
    cadena = prompt_template | llm
    
    # Invocamos pasándole el historial de mensajes
    respuesta = cadena.invoke({"chat_history": langchain_messages})
    
    return respuesta.content

# Generador de reporte de interaccion
def generar_reporte_auditoria(historial_conversacion: list) -> str:
    """
    Analiza la conversación completa acumulada y genera un reporte estructurado
    con el análisis de sentimiento y desempeño del bot auditado.
    """
    llm = inicializar_modelo()
    
    # Transformamos el historial a texto plano para que el auditor lo lea de corrido
    conversacion_texto = ""
    for rol, texto in historial_conversacion:
        nombre = "Cliente Simulado" if rol == "cliente" else "Bot Auditado"
        conversacion_texto += f"{nombre}: {texto}\n"
        
    prompt_auditor = f"""Actúa como un Consultor Experto en Aseguramiento de Calidad (QA) y Experiencia del Cliente.
Analiza la siguiente transcripción de una llamada/chat de soporte técnico y genera un reporte detallado.

[TRANSCRIPCIÓN DEL CHAT]
{conversacion_texto}

[ESTRUCTURA DEL REPORTE REQUERIDA]
1. **Resumen de la Situación**: (Breve explicación de qué problema tenía el cliente y qué ocurrió).
2. **Análisis de Sentimiento Final del Cliente**: (Determina si el cliente terminó frustrado, enojado, aliviado o satisfecho, y por qué).
3. **Evaluación del Desempeño del Bot**: (Analiza si el bot fue empático, si repitió respuestas automáticas robóticas, y si logró o no resolver el problema del cliente).
4. **Veredicto y Recomendaciones**: (¿Aprobó el bot la prueba de estrés? Brinda 2 recomendaciones técnicas para mejorar el flujo del bot).

Genera el reporte con un tono corporativo, profesional, claro y completamente en español. No uses marcas comerciales reales.
"""
    
    # Invocación directa al modelo para la tarea de análisis
    respuesta = llm.invoke(prompt_auditor)
    return respuesta.content