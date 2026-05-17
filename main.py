import os
import requests

from telegram import (
    Update,
    ReplyKeyboardMarkup
)

from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

# КЛЮЧИ
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# AI
def ask_ai(text):

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"

    data = {
        "contents": [
            {
                "parts": [
                    {
                        "text": f"""
Ты NeoHelper X ⚡

Ты:
- очень умный AI
- отвечаешь кратко
- современный стиль
- полезный
- как premium assistant

Запрос:
{text}
"""
                    }
                ]
            }
        ]
    }

    response = requests.post(
        url,
        json=data
    )

    result = response.json()

    try:
        return result["candidates"][0]["content"]["parts"][0]["text"]

    except:
        return "⚠️ AI временно недоступен"

# START
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        ["💡 Идеи", "📚 Учёба"],
        ["✍️ Тексты", "🚀 TikTok"],
        ["🧠 AI Chat"]
    ]

    markup = ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True
    )

    text = (
        "⚡ NeoHelper X PRO\n\n"
        "AI нового поколения.\n\n"
        "Выбери режим 👇"
    )

    await update.message.reply_text(
        text,
        reply_markup=markup
    )

# MESSAGES
async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_text = update.message.text

    prompts = {
        "💡 Идеи": "Придумай 5 современных идей",
        "📚 Учёба": "Объясни сложную тему просто",
        "✍️ Тексты": "Напиши красивый современный текст",
        "🚀 TikTok": "Дай вирусную TikTok идею"
    }

    prompt = prompts.get(user_text, user_text)

    answer = ask_ai(prompt)

    await update.message.reply_text(answer)

# APP
app = Application.builder().token(
    TELEGRAM_TOKEN
).build()

app.add_handler(
    CommandHandler("start", start)
)

app.add_handler(
    MessageHandler(
        filters.TEXT,
        handle
    )
)

print("NeoHelper X Online ⚡")

try:
    print("⚡ NeoHelper запускается...")
    app.run_polling()
except Exception as e:
    print("ОШИБКА:", e)