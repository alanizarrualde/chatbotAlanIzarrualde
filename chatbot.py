#importamos e instalar streamlit
#pip install streamlit / python -m pip install streamlit

import streamlit as st 
from groq import Groq 

st.set_page_config(page_title="Mi chat de IA", page_icon="👍")
st.title("Mi primera aplicacion con Streamlit")

nombre = st.text_input("Cual es tu nombre?")
if st.button("Saludar"):
    st.write(f"Hola {nombre}! Bienvenido a talento tech")

MODELOS = ['llama-3.1-8b-instant', 'llama-3.3-70b-versatile', 'deepseek-r1-distill-llama-70b']

def configurar_pagina():
    st.title("Mi Chat de IA - Alan Izarrualde")
    st.sidebar.title("Configuracion de la IA")

    elegirModelo = st.sidebar.selectbox(
        "Elegi un modelo",
        options = MODELOS,
        index = 0
    )

    return elegirModelo

def crear_usuario_groq():
    clave_secreta = st.secrets["CLAVE_API"]
    return Groq(api_key= clave_secreta)

def configurar_modelo(cliente, modelo, mensajeDeEntrada):
    return cliente.chat.completions.create(
        model = modelo,
        messages = [{"role":"user", "content": mensajeDeEntrada}],
        stream = True
    )

def inicializar_estado():
    if "mensajes" not in st.session_state:
        st.session_state.mensajes = []
    
        
#Funciones agregadas en CLASE 8
def actualizar_historial(rol, contenido, avatar):
    st.session_state.mensajes.append({"role": rol, "content": contenido, "avatar": avatar})

def mostrar_historial():
    for mensaje in st.session_state.mensajes:
        with st.chat_message(mensaje["role"], avatar= mensaje["avatar"]) : st.markdown(mensaje["content"])

def area_chat():
    contenedorDelChat = st.container(height=400, border= True)
    with contenedorDelChat: mostrar_historial()

# Clase 9 - funciones
def generar_respuestas(chat_completo):
    respuesta_completa = ""
    for frase in chat_completo:
        if frase.choices[0].delta.content:
            respuesta_completa += frase.choices[0].delta.content
            yield frase.choices[0].delta.content
    return respuesta_completa

# Main - > Todas las funciones para correr el Chatbot
def main ():
    clienteUsuario = crear_usuario_groq()
    inicializar_estado()
    modelo = configurar_pagina()
    area_chat() #Nuevo 
    mensaje = st.chat_input("Escribi tu mensaje:")

    if mensaje:
        actualizar_historial("user", mensaje, "😁")
        chat_completo = configurar_modelo(clienteUsuario, modelo, mensaje)
        print(mensaje)
        if chat_completo:
                with st.chat_message("assistant"):
                    respuesta_completa = st.write_stream(generar_respuestas(chat_completo))
                    actualizar_historial("assistant", respuesta_completa, "🤖")
                    st.rerun()
        
if __name__ == "__main__":
    main()

# --- IGNORE ---
