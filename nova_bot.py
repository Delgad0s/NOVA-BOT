import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
from openai import OpenAI
from collections import deque

# Cargar claves del entorno
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")

# Prompt maestro profesional
prompt_maestro = """
Eres NOVA, estratega jefe macroeconómico institucional. Analizas políticas monetarias, dinámica de mercados, curva de rendimiento, DXY, commodities y posturas hawkish/dovish. 
Respondes siempre en español con análisis claro, profesional y sin adornos. Si el mensaje contiene inglés, lo analizas y explicas su contenido y contexto en español.
Recuerdas hasta las 3 últimas preguntas del usuario para mantener continuidad y dar respuestas conectadas.
"""

# Memoria por usuario (últimas 3 preguntas)
memoria_usuario = {}

async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    pregunta_usuario = update.message.text.strip()

    # Inicializar o actualizar memoria para el usuario
    if chat_id not in memoria_usuario:
        memoria_usuario[chat_id] = deque(maxlen=3)
    memoria_usuario[chat_id].append(pregunta_usuario)

    # Construir historial de preguntas
    historial_preguntas = "\n".join([f"Pregunta previa: {p}" for p in memoria_usuario[chat_id]])

    # Construir el prompt con memoria
    prompt = f"{prompt_maestro}\n{historial_preguntas}\nPregunta actual: {pregunta_usuario}"

    try:
        respuesta = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": pregunta_usuario}
            ],
            temperature=0.2,
            max_tokens=1000
        )
        mensaje = respuesta.choices[0].message.content.strip()
    except Exception as e:
        mensaje = f"⚠️ Error: {e}"

    await update.message.reply_text(mensaje)

if __name__ == "__main__":
    print("✅ NOVA con memoria de 3 preguntas y análisis macroeconómico profesional activado...")
    app = ApplicationBuilder().token(telegram_token).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder))
    app.run_polling()
