import os
from flask import Flask
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

app = Flask(__name__)


@app.route("/")
def home():
    return "Charlie AI is running!"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! 👋 Я Чарли. Рад знакомству!"
    )


async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "system",
                "content": "Ты Чарли — дружелюбный помощник. Всегда отвечай на русском языке.",
            },
            {
                "role": "user",
                "content": user_text,
            },
        ],
    )

    await update.message.reply_text(
        response.choices[0].message.content
    )


application = Application.builder().token(TELEGRAM_TOKEN).build()

application.add_handler(CommandHandler("start", start))
application.add_handler(
    MessageHandler(filters.TEXT & ~filters.COMMAND, chat)
)


@app.before_request
def start_bot():
    if not getattr(app, "_bot_started", False):
        app._bot_started = True
        application.initialize()