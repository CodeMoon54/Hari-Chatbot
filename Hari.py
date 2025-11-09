import os
import gradio as gr
import google.generativeai as genai

genai.configure(api_key=os.getenv("AIzaSyAWsMXWcJD2EeCvTbmeSW7KtBus5a0MAhE"))

def responder(mensaje):
    respuesta = genai.GenerativeModel("gemini-pro").generate_content(mensaje)
    return respuesta.text

interfaz = gr.Interface(
    fn=responder,
    inputs="text",
    outputs="text",
    title="Hari",
    description="Una chica emocional creada por Zeltras."
)

interfaz.launch(server_name="0.0.0.0", server_port=int(os.environ.get("PORT", 7860)))
