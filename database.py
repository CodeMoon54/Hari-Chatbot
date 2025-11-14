import sqlite3
import json
from datetime import datetime
from typing import Dict, List, Optional, Tuple

class DatabaseManager:
    def __init__(self, db_path: str = 'hakari_memory.db'):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.create_tables()
    
    def create_tables(self):
        """Crear tablas necesarias"""
        cursor = self.conn.cursor()
        
        # Tabla de usuarios
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                nombre TEXT NOT NULL,
                fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP,
                nivel_confianza INTEGER DEFAULT 30,
                interacciones_totales INTEGER DEFAULT 0,
                ultima_visita DATETIME,
                humor_actual TEXT DEFAULT 'neutral',
                energia INTEGER DEFAULT 70,
                relacion INTEGER DEFAULT 50
            )
        ''')
        
        # Tabla de conversaciones
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversaciones (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_email TEXT NOT NULL,
                mensaje_usuario TEXT NOT NULL,
                mensaje_hakari TEXT NOT NULL,
                estado_emocional TEXT,
                fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (usuario_email) REFERENCES usuarios (email)
            )
        ''')
        
        # Tabla de memoria a largo plazo
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS memoria_largo_plazo (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_email TEXT NOT NULL,
                contenido TEXT NOT NULL,
                importancia INTEGER DEFAULT 1,
                fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (usuario_email) REFERENCES usuarios (email)
            )
        ''')
        
        # Tabla de logros
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS logros (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_email TEXT NOT NULL,
                logro_id TEXT NOT NULL,
                nombre TEXT NOT NULL,
                descripcion TEXT,
                fecha_desbloqueo DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (usuario_email) REFERENCES usuarios (email),
                UNIQUE(usuario_email, logro_id)
            )
        ''')
        
        self.conn.commit()
    
    def obtener_estado_usuario(self, email: str) -> Optional[Dict]:
        """Obtener estado completo del usuario"""
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                SELECT nombre, nivel_confianza, interacciones_totales, 
                       humor_actual, energia, relacion
                FROM usuarios WHERE email = ?
            ''', (email,))
            
            result = cursor.fetchone()
            if result:
                return {
                    'nombre': result[0],
                    'confianza': result[1],
                    'interacciones_totales': result[2],
                    'humor': result[3],
                    'energia': result[4],
                    'relacion': result[5]
                }
            return None
        except Exception as e:
            print(f"Error obteniendo estado: {e}")
            return None
    
    def actualizar_estado_usuario(self, email: str, humor: str, energia: int, relacion: int):
        """Actualizar estado del usuario"""
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                UPDATE usuarios 
                SET humor_actual = ?, energia = ?, relacion = ?,
                    interacciones_totales = interacciones_totales + 1,
                    nivel_confianza = MIN(100, nivel_confianza + 1),
                    ultima_visita = CURRENT_TIMESTAMP
                WHERE email = ?
            ''', (humor, energia, relacion, email))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error actualizando estado: {e}")
            return False
    
    def guardar_conversacion(self, usuario_email: str, mensaje_usuario: str, 
                           mensaje_hakari: str, estado_emocional: str):
        """Guardar conversación en la base de datos"""
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                INSERT INTO conversaciones 
                (usuario_email, mensaje_usuario, mensaje_hakari, estado_emocional)
                VALUES (?, ?, ?, ?)
            ''', (usuario_email, mensaje_usuario, mensaje_hakari, estado_emocional))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error guardando conversación: {e}")
            return False
    
    def obtener_ultimas_conversaciones(self, usuario_email: str, limite: int = 10) -> List[Tuple[str, str]]:
        """Obtener historial de conversaciones"""
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                SELECT mensaje_usuario, mensaje_hakari
                FROM conversaciones 
                WHERE usuario_email = ?
                ORDER BY fecha DESC
                LIMIT ?
            ''', (usuario_email, limite))
            
            historial = []
            for row in cursor.fetchall():
                historial.append([row[0], row[1]])
            
            return historial[::-1]  # Invertir para orden cronológico
        except Exception as e:
            print(f"Error obteniendo conversaciones: {e}")
            return []
    
    def guardar_memoria_importante(self, usuario_email: str, contenido: str, importancia: int = 1):
        """Guardar memoria importante a largo plazo"""
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                INSERT INTO memoria_largo_plazo (usuario_email, contenido, importancia)
                VALUES (?, ?, ?)
            ''', (usuario_email, contenido, importancia))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error guardando memoria: {e}")
            return False
    
    def obtener_memorias_importantes(self, usuario_email: str, limite: int = 3) -> List[str]:
        """Obtener memorias importantes del usuario"""
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                SELECT contenido FROM memoria_largo_plazo 
                WHERE usuario_email = ? 
                ORDER BY importancia DESC, fecha_creacion DESC 
                LIMIT ?
            ''', (usuario_email, limite))
            return [row[0] for row in cursor.fetchall()]
        except Exception as e:
            print(f"Error obteniendo memorias: {e}")
            return []
    
    def verificar_usuario_existe(self, email: str) -> bool:
        """Verificar si un usuario existe"""
        try:
            cursor = self.conn.cursor()
            cursor.execute('SELECT id FROM usuarios WHERE email = ?', (email,))
            return cursor.fetchone() is not None
        except Exception as e:
            print(f"Error verificando usuario: {e}")
            return False
    
    def registrar_usuario(self, email: str, nombre: str) -> bool:
        """Registrar nuevo usuario"""
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                INSERT INTO usuarios (email, nombre, ultima_visita)
                VALUES (?, ?, CURRENT_TIMESTAMP)
            ''', (email, nombre))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error registrando usuario: {e}")
            return False
    
    def registrar_logro(self, usuario_email: str, logro_id: str, nombre: str, descripcion: str) -> bool:
        """Registrar logro desbloqueado"""
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                INSERT OR IGNORE INTO logros (usuario_email, logro_id, nombre, descripcion)
                VALUES (?, ?, ?, ?)
            ''', (usuario_email, logro_id, nombre, descripcion))
            self.conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Error registrando logro: {e}")
            return False
    
    def obtener_logros_usuario(self, usuario_email: str) -> List[str]:
        """Obtener logros del usuario"""
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                SELECT nombre FROM logros 
                WHERE usuario_email = ? 
                ORDER BY fecha_desbloqueo DESC 
                LIMIT 5
            ''', (usuario_email,))
            return [row[0] for row in cursor.fetchall()]
        except Exception as e:
            print(f"Error obteniendo logros: {e}")
            return []
    
    def close(self):
        """Cerrar conexión a la base de datos"""
        if self.conn:
            self.conn.close()
