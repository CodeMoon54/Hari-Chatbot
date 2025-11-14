import secrets
from datetime import datetime
from typing import Dict, Optional, Tuple
from database import DatabaseManager

class SistemaAutenticacion:
    def __init__(self, db: DatabaseManager):
        self.db = db
        self.sesiones_activas = {}
    
    def registrar_usuario(self, email: str, nombre: str) -> Tuple[bool, str]:
        """Registrar nuevo usuario"""
        if self.db.verificar_usuario_existe(email):
            return False, "❌ Este email ya está registrado"
        
        if self.db.registrar_usuario(email, nombre):
            sesion_id = secrets.token_urlsafe(32)
            self.sesiones_activas[sesion_id] = {
                'email': email,
                'nombre': nombre,
                'inicio_sesion': datetime.now().isoformat(),
                'ultima_actividad': datetime.now().isoformat()
            }
            
            # Registrar logro de bienvenida
            self.db.registrar_logro(
                email, 
                'primer_conversacion', 
                '🌟 Primer Contacto', 
                'Iniciaste tu primera conversación con Hakari'
            )
            
            return True, sesion_id
        
        return False, "❌ Error al registrar usuario"
    
    def iniciar_sesion(self, email: str) -> Tuple[bool, str]:
        """Iniciar sesión de usuario existente"""
        if not self.db.verificar_usuario_existe(email):
            return False, "❌ Este email no está registrado"
        
        datos_usuario = self.db.obtener_estado_usuario(email)
        if not datos_usuario:
            return False, "❌ Error al cargar datos del usuario"
        
        sesion_id = secrets.token_urlsafe(32)
        self.sesiones_activas[sesion_id] = {
            'email': email,
            'nombre': datos_usuario['nombre'],
            'inicio_sesion': datetime.now().isoformat(),
            'ultima_actividad': datetime.now().isoformat()
        }
        
        return True, sesion_id
    
    def verificar_sesion(self, sesion_id: str) -> bool:
        """Verificar si una sesión es válida"""
        if sesion_id in self.sesiones_activas:
            # Actualizar última actividad
            self.sesiones_activas[sesion_id]['ultima_actividad'] = datetime.now().isoformat()
            return True
        return False
    
    def obtener_datos_sesion(self, sesion_id: str) -> Optional[Dict]:
        """Obtener datos de una sesión activa"""
        return self.sesiones_activas.get(sesion_id)
    
    def cerrar_sesion(self, sesion_id: str):
        """Cerrar sesión"""
        if sesion_id in self.sesiones_activas:
            del self.sesiones_activas[sesion_id]
    
    def limpiar_sesiones_expiradas(self, horas_expiracion: int = 24):
        """Limpiar sesiones expiradas"""
        ahora = datetime.now()
        sesiones_a_eliminar = []
        
        for sesion_id, datos in self.sesiones_activas.items():
            ultima_actividad = datetime.fromisoformat(datos['ultima_actividad'])
            if (ahora - ultima_actividad).total_seconds() > horas_expiracion * 3600:
                sesiones_a_eliminar.append(sesion_id)
        
        for sesion_id in sesiones_a_eliminar:
            del self.sesiones_activas[sesion_id]
        
        return len(sesiones_a_eliminar)
