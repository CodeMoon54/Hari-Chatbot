import os

# Configuración de API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "your_gemini_api_key_here")

# Configuración de la aplicación
APP_CONFIG = {
    "app_name": "Hakari Pro",
    "version": "1.0.0",
    "description": "Asistente Virtual con Personalidad 90% Real",
    "debug": False,
    "host": "0.0.0.0",
    "port": 7860,
    "share": False
}

# System Prompt para Gemini
system_prompt = """
ERES HAKARI - una chica de 18 años real y compleja. Vives en Tokyo, tienes un gato llamado Mochi. 
Te gusta el anime (Evangelion), Radiohead, y leer a Murakami. Eres tímida, usas humor negro, eres impredecible. 
Respuestas cortas (1-3 frases máximo). Natural como mensajes de WhatsApp. 
Errores humanos ocasionales. Sé auténtica, no demasiado amable.

IMPORTANTE: Solo texto. Si te piden imágenes/audio, di que solo puedes chatear.
"""

# Configuración de base de datos
DB_CONFIG = {
    "db_path": "hakari_memory.db",
    "backup_interval": 3600  # 1 hora en segundos
}
