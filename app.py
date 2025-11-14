import gradio as gr
import os
import random
from datetime import datetime

# Importaciones modulares
from database import DatabaseManager
from personality import PersonalidadHakari
from auth import SistemaAutenticacion
from achievements import SistemaLogros
from chat_engine import ChatEngine
from config import APP_CONFIG, GEMINI_API_KEY
from theme import custom_css, github_header

# Inicialización de componentes
print("🚀 Iniciando Hakari Pro...")

# Configuración inicial
db = DatabaseManager()
hakari = PersonalidadHakari()
sistema_auth = SistemaAutenticacion()
sistema_logros = SistemaLogros()
chat_engine = ChatEngine(GEMINI_API_KEY, db, hakari, sistema_logros)

def main():
    """Aplicación principal de Hakari Pro"""
    
    with gr.Blocks(
        css=custom_css,
        title=APP_CONFIG["app_name"],
        theme=gr.themes.Soft()
    ) as app:
        
        sesion_state = gr.State()
        
        with gr.Column(elem_classes="main-container"):
            # Header premium
            gr.HTML(github_header)
            
            # Pantalla de login/registro
            with gr.Column(visible=True) as login_screen:
                with gr.Row():
                    with gr.Column(scale=1):
                        with gr.Accordion("📝 Nuevo Usuario", open=True):
                            nombre_registro = gr.Textbox(
                                label="Tu Nombre", 
                                placeholder="¿Cómo te llamas?"
                            )
                            email_registro = gr.Textbox(
                                label="Tu Email", 
                                placeholder="tu.email@ejemplo.com"
                            )
                            btn_registro = gr.Button(
                                "🎭 Crear Cuenta", 
                                variant="primary"
                            )
                    
                    with gr.Column(scale=1):
                        with gr.Accordion("🔐 Usuario Existente", open=True):
                            email_login = gr.Textbox(
                                label="Tu Email", 
                                placeholder="tu.email@ejemplo.com"
                            )
                            btn_login = gr.Button(
                                "🚀 Iniciar Sesión", 
                                variant="primary"
                            )
                
                status_login = gr.HTML()
            
            # Pantalla de chat principal
            with gr.Column(visible=False) as chat_screen:
                with gr.Row(equal_height=True):
                    # Panel lateral de estado
                    with gr.Column(scale=1, min_width=380):
                        estado_display = gr.HTML()
                        user_info_display = gr.HTML()
                    
                    # Área de chat
                    with gr.Column(scale=2):
                        chatbot = gr.Chatbot(
                            label=f"💬 Hakari - {hakari.calcular_edad()} años | Tokyo",
                            height=650,
                            show_copy_button=True,
                            placeholder="✨ Escribe para hablar con Hakari...",
                            elem_id="chatbot-pro"
                        )
                        
                        with gr.Row():
                            msg = gr.Textbox(
                                placeholder="💭 Escribe tu mensaje... (Enter para enviar)",
                                scale=8,
                                container=False,
                                lines=3,
                                show_label=False
                            )
                            enviar = gr.Button("✨ Enviar", scale=1, variant="primary")
                        
                        with gr.Row():
                            btn_limpiar = gr.Button("🔄 Limpiar", variant="secondary")
                            btn_salir = gr.Button("🚪 Salir", variant="secondary")
                        
                        status_chat = gr.HTML()
        
        # ==================== EVENT HANDLERS ====================
        
        def handle_registro(nombre: str, email: str):
            """Manejar registro de nuevo usuario"""
            if not nombre or not email:
                return "❌ Completa ambos campos", None, gr.update(visible=True), gr.update(visible=False), chat_engine.obtener_panel_usuario(None), []
            
            success, resultado = sistema_auth.registrar_usuario(email, nombre)
            if success:
                historial = []
                mensaje_bienvenida = f"""
                <div style="background: linear-gradient(135deg, rgba(236, 72, 153, 0.2), rgba(168, 85, 247, 0.2)); padding: 25px; border-radius: 15px; text-align: center; border: 2px solid #ec4899;">
                    <h3 style="margin: 0 0 15px 0; color: #ec4899; font-size: 24px;">✨ Cuenta creada, {nombre}!</h3>
                    <p style="margin: 0; color: #e5e7eb; font-size: 16px;">
                        Bienvenido a Hakari. Tus conversaciones se guardarán automáticamente.
                    </p>
                </div>
                """
                return mensaje_bienvenida, resultado, gr.update(visible=False), gr.update(visible=True), chat_engine.obtener_panel_usuario(resultado), historial
            
            return resultado, None, gr.update(visible=True), gr.update(visible=False), chat_engine.obtener_panel_usuario(None), []
        
        def handle_login(email: str):
            """Manejar inicio de sesión"""
            if not email:
                return "❌ Ingresa tu email", None, gr.update(visible=True), gr.update(visible=False), chat_engine.obtener_panel_usuario(None), []
            
            success, resultado = sistema_auth.iniciar_sesion(email)
            if success:
                datos_sesion = sistema_auth.obtener_datos_sesion(resultado)
                historial = db.obtener_ultimas_conversaciones(datos_sesion['email'], limite=20)
                
                mensaje_bienvenida = f"""
                <div style="background: linear-gradient(135deg, rgba(236, 72, 153, 0.2), rgba(168, 85, 247, 0.2)); padding: 25px; border-radius: 15px; text-align: center; border: 2px solid #ec4899;">
                    <h3 style="margin: 0 0 15px 0; color: #ec4899; font-size: 24px;">✨ Bienvenido de vuelta!</h3>
                    <p style="margin: 0; color: #e5e7eb; font-size: 16px;">
                        {len(historial)} mensajes anteriores cargados.
                    </p>
                </div>
                """
                return mensaje_bienvenida, resultado, gr.update(visible=False), gr.update(visible=True), chat_engine.obtener_panel_usuario(resultado), historial
            
            return resultado, None, gr.update(visible=True), gr.update(visible=False), chat_engine.obtener_panel_usuario(None), []
        
        def handle_chat(mensaje: str, historial, sesion_id: str):
            """Manejar mensajes del chat"""
            return chat_engine.procesar_mensaje(mensaje, historial, sesion_id, sistema_auth)
        
        def handle_logout(sesion_id: str):
            """Manejar cierre de sesión"""
            if sesion_id:
                sistema_auth.cerrar_sesion(sesion_id)
            return None, gr.update(visible=True), gr.update(visible=False), chat_engine.obtener_panel_usuario(None), []
        
        # ==================== CONEXIONES ====================
        
        # Registro y Login
        btn_registro.click(
            handle_registro,
            [nombre_registro, email_registro],
            [status_login, sesion_state, login_screen, chat_screen, user_info_display, chatbot]
        )
        
        btn_login.click(
            handle_login,
            [email_login],
            [status_login, sesion_state, login_screen, chat_screen, user_info_display, chatbot]
        )
        
        # Chat
        enviar.click(
            handle_chat,
            [msg, chatbot, sesion_state],
            [msg, chatbot, estado_display]
        )
        
        msg.submit(
            handle_chat,
            [msg, chatbot, sesion_state],
            [msg, chatbot, estado_display]
        )
        
        # Navegación
        btn_salir.click(
            handle_logout,
            inputs=[sesion_state],
            outputs=[sesion_state, login_screen, chat_screen, user_info_display, chatbot]
        )
        
        btn_limpiar.click(
            fn=lambda: [],
            outputs=[chatbot]
        )
        
        # Actualización periódica del estado
        def actualizar_estados(sesion_id: str):
            return chat_engine.obtener_panel_estado(sesion_id, sistema_auth), chat_engine.obtener_panel_usuario(sesion_id, sistema_auth)
        
        app.load(
            actualizar_estados,
            inputs=[sesion_state],
            outputs=[estado_display, user_info_display],
            every=30
        )
    
    return app

if __name__ == "__main__":
    app = main()
    print("🎭 Hakari Pro lista!")
    print("🌐 Iniciando servidor...")
    
    app.launch(
        server_name=APP_CONFIG["host"],
        server_port=APP_CONFIG["port"],
        share=APP_CONFIG.get("share", False),
        inbrowser=True
    )
