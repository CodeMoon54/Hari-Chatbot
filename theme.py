"""
Tema y estilos CSS para Hakari Pro
"""

custom_css = """
.gradio-container {
    font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
    background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%);
    min-height: 100vh;
}

.main-container {
    max-width: 1400px;
    margin: 0 auto;
    padding: 20px;
    background: rgba(15, 15, 35, 0.95);
    backdrop-filter: blur(20px);
    border-radius: 24px;
    border: 1px solid rgba(236, 72, 153, 0.3);
    box-shadow: 0 25px 50px -12px rgba(236, 72, 153, 0.25);
}

/* Header Premium */
.header-pro {
    background: linear-gradient(135deg, rgba(236, 72, 153, 0.1), rgba(168, 85, 247, 0.1));
    border: 1px solid rgba(236, 72, 153, 0.3);
    border-radius: 20px;
    padding: 30px;
    margin-bottom: 30px;
    backdrop-filter: blur(10px);
}

/* Chatbot Pro */
.gr-chatbot {
    background: rgba(30, 27, 75, 0.8) !important;
    border: 2px solid rgba(236, 72, 153, 0.4) !important;
    border-radius: 20px !important;
    backdrop-filter: blur(10px);
}

.gr-chatbot .message {
    padding: 16px 20px;
    border-radius: 20px;
    margin: 12px 0;
    border: 1px solid rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
    max-width: 85%;
    line-height: 1.4;
}

.gr-chatbot .user {
    background: linear-gradient(135deg, #ec4899, #d946ef) !important;
    color: white;
    margin-left: auto;
    margin-right: 10px;
    box-shadow: 0 8px 25px -8px #ec4899;
}

.gr-chatbot .bot {
    background: rgba(30, 27, 75, 0.9) !important;
    color: #f1f5f9;
    border: 1px solid rgba(236, 72, 153, 0.3);
    margin-left: 10px;
    box-shadow: 0 8px 25px -8px rgba(30, 27, 75, 0.5);
}

/* Paneles Laterales Pro */
.sidebar-pro {
    background: linear-gradient(135deg, rgba(30, 27, 75, 0.9), rgba(55, 48, 163, 0.9));
    border: 2px solid rgba(236, 72, 153, 0.4);
    border-radius: 20px;
    padding: 20px;
    backdrop-filter: blur(15px);
    box-shadow: 0 20px 40px -20px rgba(236, 72, 153, 0.3);
}

/* Botones Pro */
.gr-button {
    background: linear-gradient(135deg, #ec4899, #d946ef) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
    padding: 12px 24px !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 15px -4px #ec4899 !important;
}

.gr-button:hover {
    background: linear-gradient(135deg, #d946ef, #ec4899) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px -8px #ec4899 !important;
}

.gr-button:active {
    transform: translateY(0) !important;
}

/* Botones secundarios */
.gr-button.secondary {
    background: rgba(30, 27, 75, 0.8) !important;
    border: 1px solid rgba(236, 72, 153, 0.4) !important;
    box-shadow: 0 2px 10px -2px rgba(236, 72, 153, 0.3) !important;
}

.gr-button.secondary:hover {
    background: rgba(236, 72, 153, 0.1) !important;
    border-color: #ec4899 !important;
}

/* Input Pro */
.gr-textbox input, .gr-textbox textarea {
    background: rgba(30, 27, 75, 0.9) !important;
    color: white !important;
    border: 2px solid rgba(236, 72, 153, 0.4) !important;
    border-radius: 16px !important;
    padding: 16px 20px !important;
    font-size: 14px !important;
    backdrop-filter: blur(10px);
    transition: all 0.3s ease;
}

.gr-textbox input:focus, .gr-textbox textarea:focus {
    border-color: #ec4899 !important;
    box-shadow: 0 0 0 3px rgba(236, 72, 153, 0.2) !important;
    background: rgba(30, 27, 75, 0.95) !important;
}

.gr-textbox input::placeholder, .gr-textbox textarea::placeholder {
    color: #9ca3af !important;
}

/* Tabs Pro */
.gr-tabs {
    background: rgba(30, 27, 75, 0.8) !important;
    border: 1px solid rgba(236, 72, 153, 0.3) !important;
    border-radius: 16px !important;
    padding: 10px !important;
}

.gr-tab-item {
    background: transparent !important;
    color: #9ca3af !important;
    border: none !important;
    border-radius: 12px !important;
    margin: 4px !important;
    padding: 10px 20px !important;
    transition: all 0.3s ease !important;
}

.gr-tab-item.selected {
    background: linear-gradient(135deg, #ec4899, #d946ef) !important;
    color: white !important;
    box-shadow: 0 4px 15px -4px #ec4899 !important;
}

/* Accordion Pro */
.gr-accordion {
    background: rgba(30, 27, 75, 0.8) !important;
    border: 1px solid rgba(236, 72, 153, 0.3) !important;
    border-radius: 16px !important;
    margin-bottom: 15px !important;
}

.gr-accordion .label {
    color: #e5e7eb !important;
    font-weight: 600 !important;
}

/* Estados Animados */
@keyframes pulse-glow {
    0% { box-shadow: 0 0 0 0 rgba(236, 72, 153, 0.7); }
    70% { box-shadow: 0 0 0 10px rgba(236, 72, 153, 0); }
    100% { box-shadow: 0 0 0 0 rgba(236, 72, 153, 0); }
}

.pulse-glow {
    animation: pulse-glow 2s infinite;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}

.fade-in {
    animation: fadeIn 0.5s ease-out;
}

/* Scrollbar Personalizado */
::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-track {
    background: rgba(30, 27, 75, 0.5);
    border-radius: 10px;
}

::-webkit-scrollbar-thumb {
    background: linear-gradient(135deg, #ec4899, #d946ef);
    border-radius: 10px;
}

::-webkit-scrollbar-thumb:hover {
    background: linear-gradient(135deg, #d946ef, #ec4899);
}

/* Responsive */
@media (max-width: 768px) {
    .main-container {
        padding: 10px;
    }
    
    .header-pro {
        padding: 20px;
    }
    
    .gr-chatbot {
        height: 500px !important;
    }
    
    .sidebar-pro {
        min-width: 100% !important;
    }
}

/* Badges y etiquetas */
.badge {
    display: inline-block;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 0.8rem;
    font-weight: 600;
    margin: 2px;
}

.badge-primary {
    background: rgba(236, 72, 153, 0.2);
    color: #f0abfc;
    border: 1px solid rgba(236, 72, 153, 0.4);
}

.badge-secondary {
    background: rgba(168, 85, 247, 0.2);
    color: #c4b5fd;
    border: 1px solid rgba(168, 85, 247, 0.4);
}

.badge-success {
    background: rgba(34, 197, 94, 0.2);
    color: #86efac;
    border: 1px solid rgba(34, 197, 94, 0.4);
}

/* Progress bars */
.progress-bar {
    background: #374151;
    border-radius: 10px;
    overflow: hidden;
    height: 8px;
}

.progress-fill {
    height: 100%;
    background: linear-gradient(135deg, #ec4899, #d946ef);
    border-radius: 10px;
    transition: width 0.5s ease;
}
"""

github_header = """
<div class="header-pro fade-in">
    <div style="text-align: center;">
        <h1 style="font-size: 3.5rem; margin: 0; background: linear-gradient(135deg, #ec4899, #a855f7, #f0abfc); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; font-weight: 800; text-shadow: 0 4px 8px rgba(0,0,0,0.3);">
            🎭 Hakari Pro
        </h1>
        <p style="color: #e5e7eb; font-size: 1.3rem; margin: 15px 0 0 0; font-weight: 300; letter-spacing: 0.5px;">
            Asistente Virtual con Personalidad 90% Real • Ciclo Menstrual • Memoria Avanzada
        </p>
        <div style="margin-top: 20px; display: flex; justify-content: center; gap: 15px; flex-wrap: wrap;">
            <span class="badge badge-primary">🧠 Personalidad Dinámica</span>
            <span class="badge badge-secondary">🩸 Ciclo Menstrual Realista</span>
            <span class="badge badge-success">💾 Memoria Persistente</span>
            <span class="badge badge-primary">🎯 Sistema de Logros</span>
            <span class="badge badge-secondary">🔐 Autenticación</span>
        </div>
        <div style="margin-top: 15px; color: #9ca3af; font-size: 0.9rem;">
            v1.0.0 • Desarrollado con Gradio & Gemini AI
        </div>
    </div>
</div>
"""

# Colores del tema para uso en código
theme_colors = {
    "primary": "#ec4899",
    "secondary": "#d946ef", 
    "accent": "#a855f7",
    "background": "#1e1b4b",
    "surface": "#312e81",
    "text_primary": "#f1f5f9",
    "text_secondary": "#9ca3af"
}
