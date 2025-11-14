from typing import Dict, List
from database import DatabaseManager

class SistemaLogros:
    def __init__(self, db: DatabaseManager):
        self.db = db
        self.logros_disponibles = {
            'primer_conversacion': {
                'nombre': '🌟 Primer Contacto', 
                'descripcion': 'Iniciaste tu primera conversación con Hakari'
            },
            'confianza_50': {
                'nombre': '💝 Confianza Básica', 
                'descripcion': 'Alcanzaste 50% de confianza'
            },
            'confianza_80': {
                'nombre': '🔐 Amistad Sólida', 
                'descripcion': 'Alcanzaste 80% de confianza'
            },
            '10_interacciones': {
                'nombre': '🎯 Conversador Persistente', 
                'descripcion': '10 interacciones completadas'
            },
            '50_interacciones': {
                'nombre': '💬 Amigo Leal', 
                'descripcion': '50 interacciones completadas'
            },
            'descubrir_anime': {
                'nombre': '📺 Otaku en Desarrollo', 
                'descripcion': 'Hablaste sobre anime'
            },
            'noche_habladora': {
                'nombre': '🌙 Noctámbulo', 
                'descripcion': 'Conversación después de medianoche'
            },
            'ciclo_comprension': {
                'nombre': '🩸 Comprensión Menstrual', 
                'descripcion': 'Preguntaste sobre su ciclo'
            },
            'conocedor_musica': {
                'nombre': '🎵 Conocedor Musical', 
                'descripcion': 'Hablaste sobre música'
            },
            'lector_avanzado': {
                'nombre': '📚 Lector Avanzado', 
                'descripcion': 'Hablaste sobre libros'
            },
            'filosofo': {
                'nombre': '🌀 Filósofo Existencial', 
                'descripcion': 'Conversación filosófica profunda'
            }
        }
    
    def verificar_logros(self, usuario_email: str, estadisticas: Dict, mensaje: str) -> List[str]:
        """Verificar y desbloquear logros"""
        logros_desbloqueados = []
        hora_actual = datetime.now().hour
        
        # Logro: Primer conversación
        if estadisticas.get('interacciones_totales', 0) >= 1:
            if self.db.registrar_logro(
                usuario_email, 'primer_conversacion',
                self.logros_disponibles['primer_conversacion']['nombre'],
                self.logros_disponibles['primer_conversacion']['descripcion']
            ):
                logros_desbloqueados.append('primer_conversacion')
        
        # Logros de confianza
        if estadisticas.get('confianza', 0) >= 50:
            if self.db.registrar_logro(
                usuario_email, 'confianza_50',
                self.logros_disponibles['confianza_50']['nombre'],
                self.logros_disponibles['confianza_50']['descripcion']
            ):
                logros_desbloqueados.append('confianza_50')
        
        if estadisticas.get('confianza', 0) >= 80:
            if self.db.registrar_logro(
                usuario_email, 'confianza_80',
                self.logros_disponibles['confianza_80']['nombre'],
                self.logros_disponibles['confianza_80']['descripcion']
            ):
                logros_desbloqueados.append('confianza_80')
        
        # Logros de interacciones
        if estadisticas.get('interacciones_totales', 0) >= 10:
            if self.db.registrar_logro(
                usuario_email, '10_interacciones',
                self.logros_disponibles['10_interacciones']['nombre'],
                self.logros_disponibles['10_interacciones']['descripcion']
            ):
                logros_desbloqueados.append('10_interacciones')
        
        if estadisticas.get('interacciones_totales', 0) >= 50:
            if self.db.registrar_logro(
                usuario_email, '50_interacciones',
                self.logros_disponibles['50_interacciones']['nombre'],
                self.logros_disponibles['50_interacciones']['descripcion']
            ):
                logros_desbloqueados.append('50_interacciones')
        
        # Logros temáticos
        if 'anime' in mensaje.lower():
            if self.db.registrar_logro(
                usuario_email, 'descubrir_anime',
                self.logros_disponibles['descubrir_anime']['nombre'],
                self.logros_disponibles['descubrir_anime']['descripcion']
            ):
                logros_desbloqueados.append('descubrir_anime')
        
        if any(palabra in mensaje.lower() for palabra in ['regla', 'menstrual', 'cólico', 'ciclo', 'periodo']):
            if self.db.registrar_logro(
                usuario_email, 'ciclo_comprension',
                self.logros_disponibles['ciclo_comprension']['nombre'],
                self.logros_disponibles['ciclo_comprension']['descripcion']
            ):
                logros_desbloqueados.append('ciclo_comprension')
        
        if any(palabra in mensaje.lower() for palabra in ['música', 'radiohead', 'canción', 'banda', 'escuchar']):
            if self.db.registrar_logro(
                usuario_email, 'conocedor_musica',
                self.logros_disponibles['conocedor_musica']['nombre'],
                self.logros_disponibles['conocedor_musica']['descripcion']
            ):
                logros_desbloqueados.append('conocedor_musica')
        
        if any(palabra in mensaje.lower() for palabra in ['libro', 'leer', 'murakami', 'lectura', 'novela']):
            if self.db.registrar_logro(
                usuario_email, 'lector_avanzado',
                self.logros_disponibles['lector_avanzado']['nombre'],
                self.logros_disponibles['lector_avanzado']['descripcion']
            ):
                logros_desbloqueados.append('lector_avanzado')
        
        if any(palabra in mensaje.lower() for palabra in ['filosofía', 'existencia', 'vida', 'universo', 'significado']):
            if self.db.registrar_logro(
                usuario_email, 'filosofo',
                self.logros_disponibles['filosofo']['nombre'],
                self.logros_disponibles['filosofo']['descripcion']
            ):
                logros_desbloqueados.append('filosofo')
        
        # Logro nocturno
        if hora_actual >= 0 and hora_actual < 6:
            if self.db.registrar_logro(
                usuario_email, 'noche_habladora',
                self.logros_disponibles['noche_habladora']['nombre'],
                self.logros_disponibles['noche_habladora']['descripcion']
            ):
                logros_desbloqueados.append('noche_habladora')
        
        return logros_desbloqueados
    
    def obtener_progreso_logros(self, usuario_email: str) -> Dict:
        """Obtener progreso de logros del usuario"""
        logros_desbloqueados = self.db.obtener_logros_usuario(usuario_email)
        total_logros = len(self.logros_disponibles)
        
        return {
            'desbloqueados': len(logros_desbloqueados),
            'total': total_logros,
            'porcentaje': (len(logros_desbloqueados) / total_logros) * 100 if total_logros > 0 else 0,
            'lista': logros_desbloqueados
        }
