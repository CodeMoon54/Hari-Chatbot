import random
import time
from typing import Dict, List, Tuple, Optional
from google import genai
from google.genai import types

class ChatEngine:
    def __init__(self, api_key: str, db, hakari, sistema_logros):
        self.api_key = api_key
        self.db = db
        self.hakari = hakari
        self.sistema_logros = sistema_logros
        self.chat = self._inicializar_gemini()
    
    def _inicializar_gemini(self):
        """Inicializar cliente de Gemini"""
        try:
            if self.api_key and self.api_key != "your_gemini_api_key_here":
                client = genai.Client(api_key=self.api_key)
                chat = client.chats.create(
                    model="gemini-2.0-flash",
                    config=types.GenerateContentConfig(
                        system_instruction="""
                        ERES HAKARI - una chica de 18 años real y compleja. 
                        Vives en Tokyo, tienes un gato llamado Mochi. 
                        Te gusta el anime (Evangelion), Radiohead, y leer a Murakami. 
                        Eres tímida, usas humor negro, eres impredecible. 
                        Respuestas cortas (1-3 frases máximo). 
                        Natural como mensajes de WhatsApp. 
                        Errores humanos ocasionales. 
                        Sé auténtica, no demasiado amable.
                        """,
                        temperature=0.9,
                        max_output_tokens=150
                    )
                )
                return chat
            else:
                print("⚠️  API Key no configurada. Usando modo simulado.")
                return None
        except Exception as e:
            print(f"❌ Error inicializando Gemini: {e}")
            return None
    
    def _error_humano(self, texto: str) -> str:
        """Añadir errores humanos realistas al texto"""
        if random.random() < 0.15:
            errores = [
                lambda t: t.replace("que", "qe", 1),
                lambda t: t + " jaja",
                lambda t: t.replace(" ", "... ", 1),
                lambda t: t.replace("yo", "yoo", 1),
                lambda t: t[:-1] + random.choice("!.") + t[-1:],
                lambda t: t.replace("pero", "pero...", 1),
                lambda t: t + " no sé",
                lambda t: t.replace("tú", "vos", 1) if "tú" in t else t,
                lambda t: t.replace("para", "pa", 1),
                lambda t: t + " creo"
            ]
            texto = random.choice(errores)(texto)
        return texto
    
    def _generar_respuesta_gemini(self, mensaje: str, estado_hakari: str) -> str:
        """Generar respuesta usando Gemini"""
        try:
            if not self.chat:
                # Modo simulado si Gemini no está disponible
                respuestas_simuladas = [
                    "hoy no estoy muy conectada... mis pensamientos están dispersos",
                    "no sé qué decir... estoy un poco fuera de lugar",
                    "mi mente está en blanco... hablamos después?",
                    "hoy no puedo pensar claramente... perdón"
                ]
                return random.choice(respuestas_simuladas)
            
            prompt_contextual = f"Estado actual: {estado_hakari}. Mensaje del usuario: {mensaje}"
            respuesta = self.chat.send_message(prompt_contextual)
            respuesta_final = respuesta.text
            
            # Limitar longitud
            oraciones = respuesta_final.split('. ')
            if len(oraciones) > 2:
                respuesta_final = '. '.join(oraciones[:2]) + '.'
            
            return respuesta_final
            
        except Exception as e:
            print(f"❌ Error en Gemini: {e}")
            return "💫 Mis pensamientos están dispersos... ¿podemos intentarlo de nuevo?"
    
    def procesar_mensaje(self, mensaje: str, historial: List, sesion_id: str, sistema_auth) -> Tuple[str, List, str]:
        """Procesar un mensaje y generar respuesta"""
        if not sesion_id or not mensaje.strip():
            return "", historial, self.obtener_panel_estado(sesion_id, sistema_auth)
        
        if not sistema_auth.verificar_sesion(sesion_id):
            return "", historial, self.obtener_panel_estado(sesion_id, sistema_auth)
        
        datos_sesion = sistema_auth.obtener_datos_sesion(sesion_id)
        estado_usuario = self.db.obtener_estado_usuario(datos_sesion['email'])
        
        if not estado_usuario:
            return "💫 Algo pasó con mi memoria... ¿podemos empezar de nuevo?", historial, self.obtener_panel_estado(sesion_id, sistema_auth)
        
        # Actualizar estado de Hakari
        estado_hakari = self.hakari.actualizar_estado_dinamico(mensaje, estado_usuario)
        
        # Buscar respuesta rápida
        respuesta_rapida = self.hakari.obtener_respuesta_rapida(mensaje, estado_usuario)
        if respuesta_rapida:
            respuesta_final = respuesta_rapida
        else:
            # Generar respuesta con Gemini
            respuesta_final = self._generar_respuesta_gemini(mensaje, estado_hakari)
        
        # Aplicar errores humanos
        respuesta_final = self._error_humano(respuesta_final)
        
        # Añadir elementos contextuales
        relacion = estado_usuario.get('relacion', 50)
        
        # Referencias a memoria (solo con suficiente confianza)
        if relacion > 40 and random.random() < 0.25:
            memorias = self.db.obtener_memorias_importantes(datos_sesion['email'], 2)
            if memorias:
                respuesta_final += f"<br><small><i>me acordé cuando dijiste \"{random.choice(memorias)}\"...</i></small>"
        
        # Mencionar caprichos actuales
        if random.random() < 0.2:
            respuesta_final += f"<br><small>quiero {self.hakari.capricho_actual} ahora...</small>"
        
        # Guardar información importante en memoria
        if len(mensaje) > 20 or any(palabra in mensaje.lower() for palabra in ['importante', 'recuerda', 'nunca olvidar', 'siempre']):
            self.db.guardar_memoria_importante(datos_sesion['email'], mensaje, 2)
        
        # Actualizar estadísticas del usuario
        self._actualizar_estadisticas_usuario(datos_sesion['email'], estado_hakari, mensaje)
        
        # Guardar conversación
        self.db.guardar_conversacion(datos_sesion['email'], mensaje, respuesta_final, estado_hakari)
        
        # Verificar logros
        self.sistema_logros.verificar_logros(datos_sesion['email'], estado_usuario, mensaje)
        
        nuevo_historial = historial + [[mensaje, respuesta_final]]
        return "", nuevo_historial, self.obtener_panel_estado(sesion_id, sistema_auth)
    
    def _actualizar_estadisticas_usuario(self, email: str, estado_hakari: str, mensaje: str):
        """Actualizar estadísticas del usuario basadas en la interacción"""
        estado_usuario = self.db.obtener_estado_usuario(email)
        if not estado_usuario:
            return
        
        hora_actual = datetime.now().hour
        
        # Calcular nueva energía
       
