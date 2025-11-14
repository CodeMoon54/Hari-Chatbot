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
        nueva_energia = max(10, estado_usuario['energia'] - random.randint(1, 5))
        if hora_actual > 22 or hora_actual < 6:
            nueva_energia = max(5, nueva_energia - 10)
        
        # Calcular nueva relación
        nueva_relacion = estado_usuario['relacion']
        if len(mensaje) > 5:
            incremento = random.randint(1, 3)
            # Bonus por conversaciones nocturnas
            if hora_actual > 22 or hora_actual < 6:
                incremento += 2
            nueva_relacion = min(100, nueva_relacion + incremento)
        
        if any(palabra in mensaje.lower() for palabra in ['chau', 'adiós', 'no quiero', 'molesto', 'odio']):
            nueva_relacion = max(0, nueva_relacion - 5)
        
        self.db.actualizar_estado_usuario(email, estado_hakari, nueva_energia, nueva_relacion)
    
    def obtener_panel_estado(self, sesion_id: str, sistema_auth) -> str:
        """Generar panel de estado de Hakari"""
        if not sesion_id or not sistema_auth.verificar_sesion(sesion_id):
            return """
            <div class="sidebar-pro" style="text-align: center;">
                <div style="font-size: 48px; margin-bottom: 15px;">🌙</div>
                <div style="font-weight: bold; color: #e5e7eb; font-size: 18px;">Hakari está esperando...</div>
                <div style="color: #9ca3af; font-size: 14px; margin-top: 8px;">Inicia sesión para comenzar</div>
            </div>
            """
        
        datos_sesion = sistema_auth.obtener_datos_sesion(sesion_id)
        estado_usuario = self.db.obtener_estado_usuario(datos_sesion['email'])
        
        if not estado_usuario:
            return """
            <div class="sidebar-pro" style="text-align: center;">
                <div style="color: #ef4444; font-size: 14px;">Error cargando estado</div>
            </div>
            """
        
        info_hakari = self.hakari.obtener_info_estado()
        estado_info = info_hakari['estado_info']
        ciclo_info = info_hakari['ciclo_menstrual']
        
        fase_emoji = {"menstruacion": "🩸", "folicular": "🌸", "ovulacion": "💫", "lutea": "🌙"}
        fase_nombre = {
            "menstruacion": "Menstruación", 
            "folicular": "Fase Folicular", 
            "ovulacion": "Ovulación", 
            "lutea": "Fase Lútea"
        }
        
        return f"""
        <div class="sidebar-pro">
            <div style="text-align: center; margin-bottom: 20px;">
                <div style="font-size: 42px; margin-bottom: 10px;">{estado_info['emoji']}</div>
                <div style="font-weight: 800; color: {estado_info['color']}; font-size: 20px; margin-bottom: 5px;">
                    {info_hakari['estado_actual'].title()}
                </div>
                <div style="color: #d1d5db; font-size: 14px; margin-bottom: 15px;">
                    {estado_info['desc']}
                </div>
            </div>
            
            <!-- Info Ciclo Menstrual -->
            <div style="background: rgba(236, 72, 153, 0.15); padding: 15px; border-radius: 14px; margin-bottom: 20px; border: 1px solid rgba(236, 72, 153, 0.3);">
                <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 10px;">
                    <span style="color: #f0abfc; font-weight: 600; font-size: 14px;">
                        {fase_emoji[ciclo_info['fase_actual']]} {fase_nombre[ciclo_info['fase_actual']]}
                    </span>
                    <span style="color: #9ca3af; font-size: 12px;">Día {(datetime.now().day % 28) + 1}/28</span>
                </div>
                <div style="color: #c4b5fd; font-size: 12px; margin-bottom: 8px;">
                    Dolor: {ciclo_info['dolor']}/10
                </div>
                <div style="color: #86efac; font-size: 11px;">
                    {', '.join(ciclo_info['sintomas'][:2])}
                </div>
            </div>
            
            <!-- Stats Usuario -->
            <div style="background: rgba(30, 27, 75, 0.8); padding: 15px; border-radius: 14px; border: 1px solid rgba(255, 255, 255, 0.1);">
                <div style="color: #e5e7eb; font-weight: 600; margin-bottom: 12px; font-size: 14px;">📊 Tu Progreso</div>
                
                <div style="margin-bottom: 12px;">
                    <div style="display: flex; justify-content: between; margin-bottom: 5px;">
                        <span style="color: #9ca3af; font-size: 12px;">Confianza</span>
                        <span style="color: #ec4899; font-size: 12px; font-weight: 600;">{estado_usuario['confianza']}%</span>
                    </div>
                    <div style="background: #374151; border-radius: 10px; height: 8px; overflow: hidden;">
                        <div style="background: linear-gradient(135deg, #ec4899, #d946ef); width: {estado_usuario['confianza']}%; height: 100%;"></div>
                    </div>
                </div>
                
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; font-size: 12px;">
                    <div style="text-align: center;">
                        <div style="color: #86efac; font-weight: 600;">{estado_usuario['energia']}%</div>
                        <div style="color: #9ca3af;">Energía</div>
                    </div>
                    <div style="text-align: center;">
                        <div style="color: #60a5fa; font-weight: 600;">{estado_usuario['interacciones_totales']}</div>
                        <div style="color: #9ca3af;">Interacciones</div>
                    </div>
                </div>
            </div>
            
            <!-- Capricho Actual -->
            <div style="margin-top: 15px; padding: 12px; background: rgba(168, 85, 247, 0.1); border-radius: 12px; border: 1px solid rgba(168, 85, 247, 0.3);">
                <div style="color: #c4b5fd; font-size: 12px; text-align: center;">
                    <span style="font-weight: 600;">🎯 Capricho actual:</span><br>
                    {info_hakari['capricho_actual']}
                </div>
            </div>
        </div>
        """
    
    def obtener_panel_usuario(self, sesion_id: str, sistema_auth) -> str:
        """Generar panel de información del usuario"""
        if not sesion_id or not sistema_auth.verificar_sesion(sesion_id):
            return """
            <div class="sidebar-pro" style="text-align: center;">
                <div style="font-weight: bold; color: #e5e7eb;">👤 No has iniciado sesión</div>
            </div>
            """
        
        datos_sesion = sistema_auth.obtener_datos_sesion(sesion_id)
        estado_usuario = self.db.obtener_estado_usuario(datos_sesion['email'])
        
        if not estado_usuario:
            return """
            <div class="sidebar-pro" style="text-align: center;">
                <div style="font-weight: bold; color: #e5e7eb;">👤 Error al cargar datos</div>
            </div>
            """
        
        logros = self.db.obtener_logros_usuario(datos_sesion['email'])
        progreso = self.sistema_logros.obtener_progreso_logros(datos_sesion['email'])
        
        logros_html = ""
        if logros:
            logros_html = f"""
            <div style="margin-top: 15px; padding-top: 15px; border-top: 1px solid #4b5563;">
                <div style="font-size: 12px; color: #9ca3af; margin-bottom: 8px;">
                    <strong>🏆 Logros ({progreso['desbloqueados']}/{progreso['total']})</strong>
                </div>
                <div style="font-size: 11px; color: #d946ef;">
                    {' • '.join(logros[:3])}
                    {f'<br>+ {len(logros) - 3} más...' if len(logros) > 3 else ''}
                </div>
            </div>
            """
        
        return f"""
        <div class="sidebar-pro">
            <div style="font-weight: bold; color: #ec4899; font-size: 16px; margin-bottom: 8px;">
                👤 {estado_usuario['nombre']}
            </div>
            <div style="font-size: 12px; color: #e5e7eb; margin-bottom: 12px; word-break: break-all;">
                {datos_sesion['email']}
            </div>
            
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px; font-size: 11px; color: #9ca3af; margin: 10px 0;">
                <div style="text-align: center;">
                    <div style="color: #ec4899; font-weight: 600; font-size: 14px;">{estado_usuario['confianza']}%</div>
                    <div>Confianza</div>
                </div>
                <div style="text-align: center;">
                    <div style="color: #60a5fa; font-weight: 600; font-size: 14px;">{estado_usuario['interacciones_totales']}</div>
                    <div>Interacciones</div>
                </div>
            </div>
            
            <div style="background: rgba(30, 27, 75, 0.8); padding: 10px; border-radius: 10px; margin: 8px 0;">
                <div style="display: flex; justify-content: space-between; font-size: 11px; margin-bottom: 5px;">
                    <span>Relación:</span>
                    <span style="color: #86efac; font-weight: 600;">{estado_usuario['relacion']}%</span>
                </div>
                <div style="background: #374151; border-radius: 5px; height: 6px; overflow: hidden;">
                    <div style="background: #86efac; width: {estado_usuario['relacion']}%; height: 100%;"></div>
                </div>
            </div>
            {logros_html}
        </div>
        """
