import os
import requests
import telebot

# КЛЮЧИ
BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# BOT
bot = telebot.TeleBot(BOT_TOKEN)

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
- очень умный
- современный
- полезный
- отвечаешь кратко

Запрос:
{text}
"""
                    }
                ]
            }
        ]
    }

    response = requests.post(url, json=data)

    result = response.json()

    try:
        return result["candidates"][0]["content"]["parts"][0]["text"]

    except:
        return "⚠️ AI ошибка"

# START
@bot.message_handler(commands=['start'])
def start(message):

    bot.reply_to(
        message,
        "⚡ NeoHelper X Online\n\nНапиши любой вопрос 👇"
    )

# MESSAGE
@bot.message_handler(func=lambda message: True)
def handle(message):

    user_text = message.text

    answer = ask_ai(user_text)

    bot.reply_to(message, answer)

print("⚡ NeoHelper работает")

# RUN
bot.infinity_polling()