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
    
#colores y personalizados

# 💅 Estilos HTML + CSS personalizados
st.markdown("""
    <style>
        /* ===== Fondo general ===== */
        body {
            background-color: #FA8072; /* Rosa salmón */
            color: #FFFFFF; /* Texto blanco */
            font-family: 'Poppins', Montserrat, sans-serif;
        }

        /* Fondo general de la app */
        .stApp {
            background-color: #FA8072; /* Rosa salmón */
        }

        /* ===== Títulos ===== */
        h1, h2, h3, h4 {
            color: #FFFFFF; /* Blanco puro */
            text-align: center;
            text-shadow: 0px 0px 10px rgba(255, 255, 255, 0.4);
        }

        /* ===== Entradas de texto ===== */
        .stTextInput > div > div > input, .stTextArea > div > textarea {
            background-color: #f28a7e; /* Rosa más suave */
            color: #FFFFFF;
            border: 1px solid #ffffff;
            border-radius: 10px;
            padding: 10px;
        }

        /* ===== Botones ===== */
        .stButton>button {
            background-color: #ffffff; /* Blanco */
            color: #FA8072; /* Rosa salmón */
            border: none;
            border-radius: 10px;
            padding: 10px 25px;
            font-weight: 700;
            font-size: 1em;
            transition: 0.3s ease-in-out;
            box-shadow: 0px 4px 10px rgba(255, 255, 255, 0.4);
        }

        .stButton>button:hover {
            background-color: #ffe6e1; /* Blanco rosado al pasar el mouse */
            transform: scale(1.05);
        }

        /* ===== Mensajes del bot ===== */
        .bot-message {
            background-color: #f49d90;
            color: #FFFFFF;
            border-radius: 10px;
            padding: 10px;
            margin-top: 10px;
        }

        /* ===== Mensajes del usuario ===== */
        .user-message {
            background-color: #f6b2a7;
            color: #FFFFFF;
            border-radius: 10px;
            padding: 10px;
            margin-top: 10px;
            text-align: right;
        }

        /* ===== Enlaces ===== */
        a {
            color: #FFFFFF;
            text-decoration: underline;
        }

        a:hover {
            color: #ffe6e1;
        }

        /* ===== Barra lateral ===== */
        section[data-testid="stSidebar"] {
            background-color: #f5978b;
            color: #FFFFFF;
        }

    </style>
""", unsafe_allow_html=True)
# --- IGNORE ---