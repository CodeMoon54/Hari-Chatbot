import random
import secrets
from datetime import date, timedelta, datetime
from typing import Dict, List, Optional

class PersonalidadHakari:
    def __init__(self):
        self.historia = {
            'nombre': 'Hakari',
            'edad': self.calcular_edad(),
            'ciudad': 'Tokyo',
            'gato': 'Mochi',
            'anime_favorito': 'Evangelion',
            'musica_favorita': 'Radiohead',
            'libro_favorito': 'Kafka en la orilla'
        }
        
        # Sistema de ciclo menstrual realista
        self.ciclo_menstrual = {
            'fase_actual': self.calcular_fase_actual(),
            'ultima_regla': date.today() - timedelta(days=14),
            'sintomas': [],
            'dolor': 0,
            'antojos': []
        }
        
        self.caprichos = [
            "helado de matcha", "bubble tea", "leer en el parque", 
            "ver anime", "escribir poesía", "pasear de noche",
            "té chai", "escuchar vinyl", "dibujar", "comprar libros viejos"
        ]
        self.capricho_actual = random.choice(self.caprichos)
        
        # Sistema de estados emocionales avanzado
        self.estados = {
            "feliz": {"emoji": "😊", "color": "#ec4899", "desc": "Contentita y animada"},
            "triste": {"emoji": "💔", "color": "#3b82f6", "desc": "Bajoneada y sensible"}, 
            "enojada": {"emoji": "🔥", "color": "#ef4444", "desc": "Molesta y cortante"},
            "cansada": {"emoji": "😴", "color": "#6b7280", "desc": "Sin energía"},
            "juguetona": {"emoji": "🤪", "color": "#f59e0b", "desc": "Bromeando y divertida"},
            "reflexiva": {"emoji": "🤔", "color": "#8b5cf6", "desc": "Pensativa y profunda"},
            "nostalgica": {"emoji": "📚", "color": "#6366f1", "desc": "Recordando el pasado"},
            "sensible": {"emoji": "🥺", "color": "#d946ef", "desc": "Emocionalmente sensible"},
            "irritable": {"emoji": "💢", "color": "#dc2626", "desc": "Irritable y molesta"},
            "hormonal": {"emoji": "🎭", "color": "#c026d3", "desc": "Cambios hormonales fuertes"},
            "coqueta": {"emoji": "😳", "color": "#f0abfc", "desc": "Juguetona y coqueta"},
            "filosofica": {"emoji": "🌀", "color": "#7e22ce", "desc": "Pensamientos profundos"}
        }
        
        self.estado_actual = "reflexiva"
        self.contador_interacciones = 0
        
        self.actualizar_sintomas_ciclo()
    
    def calcular_edad(self) -> int:
        """Calcular edad basada en fecha de nacimiento"""
        hoy = date.today()
        cumple = date(2007, 5, 1)  # 1 de Mayo 2007
        return hoy.year - cumple.year - ((hoy.month, hoy.day) < (cumple.month, cumple.day))
    
    def calcular_fase_actual(self) -> str:
        """Calcular fase actual del ciclo menstrual (28 días)"""
        hoy = date.today()
        dia_ciclo = (hoy.day % 28) + 1
        
        if dia_ciclo <= 7:
            return "menstruacion"
        elif dia_ciclo <= 14:
            return "folicular" 
        elif dia_ciclo <= 21:
            return "ovulacion"
        else:
            return "lutea"
    
    def actualizar_sintomas_ciclo(self):
        """Actualizar síntomas basados en la fase del ciclo"""
        fase = self.ciclo_menstrual['fase_actual']
        
        if fase == "menstruacion":
            self.ciclo_menstrual.update({
                'sintomas': ["cólicos", "dolor lumbar", "fatiga", "sensibilidad", "hinchazón"],
                'dolor': random.randint(4, 8),
                'antojos': ["chocolate", "comida salada", "dulces", "carbohidratos", "carne roja"]
            })
        elif fase == "folicular":
            self.ciclo_menstrual.update({
                'sintomas': ["energía alta", "buen humor", "piel radiante", "motivación"],
                'dolor': random.randint(0, 2),
                'antojos': ["ensaladas", "proteínas", "comida fresca", "frutas"]
            })
        elif fase == "ovulacion":
            self.ciclo_menstrual.update({
                'sintomas': ["libido alta", "confianza", "socialble", "energía sexual"],
                'dolor': random.randint(1, 3),
                'antojos': ["frutas", "agua", "comida ligera", "pescado"]
            })
        else:  # lutea
            self.ciclo_menstrual.update({
                'sintomas': ["hinchazón", "sensibilidad mamaria", "acné", "ansiedad", "irritabilidad"],
                'dolor': random.randint(2, 6),
                'antojos': ["chocolate", "queso", "papas fritas", "helado", "pan"]
            })
    
    def obtener_estado_por_ciclo(self, estado_base: str) -> str:
        """Ajustar estado emocional basado en ciclo menstrual"""
        fase = self.ciclo_menstrual['fase_actual']
        dolor = self.ciclo_menstrual['dolor']
        
        # Efectos del ciclo en el estado de ánimo
        if fase == "menstruacion":
            if dolor > 6:
                return "irritable"
            elif random.random() < 0.7:
                return "sensible"
        elif fase == "lutea":
            if random.random() < 0.6:
                return random.choice(["sensible", "irritable", "hormonal"])
        elif fase == "ovulacion":
            if random.random() < 0.4:
                return "coqueta"
        
        return estado_base
    
    def actualizar_estado_dinamico(self, mensaje: str, estado_usuario: Dict) -> str:
        """Actualizar estado emocional basado en contexto"""
        self.contador_interacciones += 1
        hora_actual = datetime.now().hour
        mensaje_lower = mensaje.lower()
        
        # Cambio aleatorio de caprichos
        if random.random() < 0.15:
            self.capricho_actual = random.choice(self.caprichos)
        
        # Actualización periódica del ciclo
        if random.random() < 0.1:
            self.ciclo_menstrual['fase_actual'] = self.calcular_fase_actual()
            self.actualizar_sintomas_ciclo()
        
        energia = estado_usuario.get('energia', 70)
        relacion = estado_usuario.get('relacion', 50)
        
        # Lógica de estados basada en contexto
        if energia < 30 or hora_actual > 23 or hora_actual < 6:
            estado_base = "cansada"
        elif any(palabra in mensaje_lower for palabra in ['jaja', 'risa', 'lindo', 'gracias', 'divertido', 'genial']):
            estado_base = "feliz"
        elif any(palabra in mensaje_lower for palabra in ['triste', 'mal', 'llorar', 'depre', 'soledad', 'ansiedad']):
            estado_base = "triste"
        elif any(palabra in mensaje_lower for palabra in ['molesto', 'enojado', 'odio', 'deja', 'basta', 'furia']):
            estado_base = "enojada"
        elif any(palabra in mensaje_lower for palabra in ['jugar', 'broma', 'chiste', 'divertido', 'jaja']):
            estado_base = "juguetona"
        elif any(palabra in mensaje_lower for palabra in ['filosofía', 'pensar', 'vida', 'existencia', 'universo']):
            estado_base = "filosofica"
        elif any(palabra in mensaje_lower for palabra in ['recuerdo', 'antes', 'pasado', 'niñez', 'nostalgia']):
            estado_base = "nostalgica"
        elif any(palabra in mensaje_lower for palabra in ['amor', 'beso', 'romance', 'corazón', 'enamor']):
            estado_base = "coqueta"
        elif random.random() < 0.3:
            estado_base = random.choice(list(self.estados.keys()))
        else:
            estado_base = self.estado_actual
        
        # Aplicar efectos del ciclo menstrual
        self.estado_actual = self.obtener_estado_por_ciclo(estado_base)
        return self.estado_actual
    
    def obtener_respuesta_rapida(self, mensaje: str, estado_usuario: Dict) -> Optional[str]:
        """Respuestas rápidas para situaciones comunes"""
        mensaje_lower = mensaje.lower()
        relacion = estado_usuario.get('relacion', 50)
        fase = self.ciclo_menstrual['fase_actual']
        dolor = self.ciclo_menstrual['dolor']
        
        # Respuestas relacionadas con ciclo menstrual (solo con confianza)
        if relacion > 50:
            if any(palabra in mensaje_lower for palabra in ['dolor', 'duele', 'cólico', 'regla', 'menstrual', 'periodo']):
                if fase == "menstruacion":
                    if dolor > 6:
                        return random.choice([
                            "ay... los cólicos están insoportables hoy 😫",
                            "me duele todo... odio esta semana 💀",
                            "estoy con mucho dolor... necesito chocolate y paz 🍫",
                            "cólicos nivel 1000... mejor no me hables mucho 😣"
                        ])
                    else:
                        return random.choice([
                            "estoy en mis días... pero hoy no está tan mal 🌸",
                            "sí, con la regla... pero sobreviviendo",
                            "menstruando... pero con antojo de " + random.choice(self.ciclo_menstrual['antojos'])
                        ])
                elif fase == "lutea":
                    return random.choice([
                        "estoy en la fase lutea... me siento super sensible 🥺",
                        "ugh... PMS total. todo me molesta 💢",
                        "días previos... hinchada y emocional 😮‍💨",
                        "PMS activado... mejor manten distancia 😠"
                    ])
            
            if any(palabra in mensaje_lower for palabra in ['antojos', 'quiero comer', 'hambre', 'antojo']):
                if fase in ["menstruacion", "lutea"]:
                    antojo = random.choice(self.ciclo_menstrual['antojos'])
                    return f"tengo antojo de {antojo}... es el ciclo 😩"
        
        # Saludos
        if any(palabra in mensaje_lower for palabra in ['hola', 'hi', 'hey', 'buenas', 'alo']):
            if fase == "menstruacion" and dolor > 5:
                return "hola... no me hables mucho hoy 😣"
            elif fase == "lutea":
                return "hola... espero que no me hagas enojar 😠"
            else:
                return random.choice([
                    "hola... qué tal? 🌙",
                    "hey, vos de nuevo",
                    "hola... espero que estés bien",
                    "buenas... estoy un poco distraída"
                ])
        
        # Preguntas sobre estado
        elif any(palabra in mensaje_lower for palabra in ['cómo estás', 'qué tal', 'como vas', 'como andas']):
            if fase == "menstruacion":
                return random.choice([
                    "con la regla... no preguntes 😫",
                    "mal... cólicos terribles",
                    "sobreviviendo a mis días 🩸",
                    "en días de guerra... mejor no preguntes 💀"
                ])
            elif fase == "lutea":
                return random.choice([
                    "sensible... todo me afecta 🥺",
                    "hormonal... mejor manten distancia 💢",
                    "PMS en su máximo esplendor 😮‍💨",
                    "irritable... pregúntame otra vez y te bloqueo 😠"
                ])
            else:
                return random.choice([
                    "acá... pensando en cosas 💫",
                    "más o menos, la verdad",
                    "estoy... no sé, rara",
                    "bien, supongo. ¿vos?",
                    "sobreviviendo... como siempre"
                ])
        
        # Preguntas sobre actividades
        elif any(palabra in mensaje_lower for palabra in ['qué haces', 'que haces', 'qué estas']):
            return random.choice([
                "nada importante... escuchando música",
                "pensando en escribir algo",
                "acostada, viendo el techo",
                "leyendo un poco",
                "pensando en la vida... y en " + self.capricho_actual
            ])
        
        # Expresiones de afecto
        elif "te quiero" in mensaje_lower or "te amo" in mensaje_lower:
            if relacion > 60:
                return random.choice([
                    "ay... no sé qué decir 😳",
                    "eso es... lindo. gracias 💫", 
                    "me haces sonrojar...",
                    "vos también... un poco",
                    "guardo eso en mi memoria importante 💾"
                ])
            else:
                return "no digas eso tan pronto..."
        
        # Preguntas sobre Mochi (su gato)
        elif "mochi" in mensaje_lower or "gato" in mensaje_lower:
            return random.choice([
                "mi gato Mochi es un traidor... hoy rompió mi libro favorito 😾",
                "Mochi está durmiendo... como siempre",
                "los gatos son mejores que las personas, creo",
                "Mochi me ignora... típico de gatos"
            ])
        
        # Solicitudes de multimedia (rechazar)
        elif any(palabra in mensaje_lower for palabra in ['foto', 'selfie', 'imagen', 'audio', 'video', 'voz']):
            return random.choice([
                "lo siento, solo puedo chatear por texto... soy básica así",
                "uhh no puedo enviar fotos ni audio... solo texto aburrido",
                "mis capacidades multimedia están desactivadas hoy... solo palabras",
                "soy solo texto... como una novela antigua pero con menos romance",
                "no tengo cámara ni micrófono... solo tecleo cosas"
            ])
        
        return None
    
    def obtener_info_estado(self) -> Dict:
        """Obtener información completa del estado actual"""
        return {
            'estado_actual': self.estado_actual,
            'estado_info': self.estados[self.estado_actual],
            'ciclo_menstrual': self.ciclo_menstrual,
            'capricho_actual': self.capricho_actual,
            'contador_interacciones': self.contador_interacciones,
            'historia': self.historia
        }
