import streamlit as st
from simulador import simular_respuesta_cliente, generar_reporte_auditoria 

# ============================================================
# 1. CONFIGURACIÓN DE LA PÁGINA E INTERFAZ
# ============================================================
st.set_page_config(
    page_title="Simulador de Clientes IA - EvalBot",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Agente Simulador de Clientes (Auditor de Bots)")
st.caption("Herramienta avanzada para estresar y probar bots de atención al cliente empleando modismos ecuatorianos.")

# ============================================================
# 2. PANEL LATERAL (PARAMETRIZACIÓN DEL SIMULADOR)
# ============================================================
st.sidebar.header("⚙️ Configuración del Cliente")

humor = st.sidebar.selectbox(
    "Estado de Ánimo:",
    ["Enojado", "Frustrado", "Preocupado", "Feliz", "Amable"]
)

region = st.sidebar.radio(
    "Región de Ecuador (Acento/Estilo):",
    ["Costa (Guayaquil/Manabí)", "Sierra (Quito/Cuenca)"]
)

# Casos de prueba preconfigurados
caso_seleccionado = st.sidebar.selectbox(
    "Caso Técnico Ficticio:",
    [
        "Lentitud extrema en horas de teletrabajo (6 PM a 10 PM)",
        "Intermitencia constante (El módem parpadea y se cae la señal)",
        "Cobro desconocido en la factura mensual",
        "Personalizado (Escribir abajo)"
    ]
)

if caso_seleccionado == "Personalizado (Escribir abajo)":
    caso_tecnico = st.sidebar.text_area("Describa el caso personalizado:", "El internet se corta cada vez que llueve.")
else:
    caso_tecnico = caso_seleccionado

# Botón para reiniciar la simulación
if st.sidebar.button("🔄 Reiniciar Conversación"):
    st.session_state.historial = []
    if "reporte_guardado" in st.session_state:
        del st.session_state["reporte_guardado"] # Limpia el reporte viejo
    st.rerun()

# ============================================================
# 3. GESTIÓN DEL ESTADO DE LA CONVERSACIÓN (MEMORIA DE STREAMLIT)
# ============================================================
# Streamlit se ejecuta de arriba a abajo cada vez que interactuamos. 
# Usamos st.session_state para que el historial no se borre.
if "historial" not in st.session_state:
    st.session_state.historial = []

# ============================================================
# 4. ÁREA DEL CHAT (INTERACCIÓN)
# ============================================================
st.subheader("💬 Ventana de Pruebas")
st.info(
    f"**Configuración Activa:** Cliente *{humor}* | Región: *{region}* \n\n"
    f"**Problema configurado:** {caso_tecnico}"
)

# Dibujar los mensajes del historial en la pantalla
for rol, texto in st.session_state.historial:
    if rol == "cliente":
        with st.chat_message("assistant", avatar="🧑‍💼"):
            st.write(texto)
    else:
        with st.chat_message("user", avatar="🤖"):
            st.write(texto)

# Entrada de texto: Aquí el evaluador escribe LO QUE EL BOT LE RESPONDIÓ al cliente
if respuesta_del_bot := st.chat_input("Escribe aquí la respuesta que dio tu bot de soporte..."):
    
    # 1. Registrar lo que dijo el bot en el historial
    st.session_state.historial.append(("bot", respuesta_del_bot))
    
    # Mostrarlo inmediatamente en pantalla
    with st.chat_message("user", avatar="🤖"):
        st.write(respuesta_del_bot)
        
    # 2. Llamar al simulador (Gemma 4) para generar la reacción del cliente
    with st.spinner("El cliente está pensando su respuesta..."):
        frase_cliente = simular_respuesta_cliente(
            humor=humor,
            region=region,
            caso_tecnico=caso_tecnico,
            historial_conversacion=st.session_state.historial
        )
        
    # 3. Registrar la reacción del cliente en el historial y mostrarla
    st.session_state.historial.append(("cliente", frase_cliente))
    with st.chat_message("assistant", avatar="🧑‍💼"):
        st.write(frase_cliente)

# ============================================================
# 5. SECCIÓN DE EVALUACIÓN Y REPORTE FINAL (EN SIDEBAR)
# ============================================================
st.sidebar.markdown("---")
st.sidebar.subheader("📊 Auditoría de Calidad")

# Solo permitimos auditar si ya hay mensajes en la conversación
if len(st.session_state.historial) > 0:
    if st.sidebar.button("📈 Generar Auditoría Final"):
        with st.sidebar.spinner("Analizando chat..."):
            reporte_final = generar_reporte_auditoria(st.session_state.historial)
            
        # Guardamos el reporte en el estado de sesión para que no se borre al dar clic en la app
        st.session_state.reporte_guardado = reporte_final

    # Si ya se generó un reporte, lo mostramos de forma compacta en la barra lateral
    if "reporte_guardado" in st.session_state:
        st.sidebar.success("✅ Auditoría Completada")
        st.sidebar.markdown(st.session_state.reporte_guardado)
else:
    st.sidebar.caption("Interactúa en el chat para poder generar la auditoría de calidad.")