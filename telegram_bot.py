
import os
import logging
from dotenv import load_dotenv

try:
    from telegram import Update
    from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
except ModuleNotFoundError:
    raise SystemExit("❌ 'python-telegram-bot' modulu tapılmadı. Railway Environment'a əlavə et: python-telegram-bot")

try:
    import openai
except ModuleNotFoundError:
    raise SystemExit("❌ 'openai' modulu tapılmadı. Railway Environment'a əlavə et: openai")

logging.basicConfig(level=logging.INFO)
load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
RAILWAY_URL = os.getenv("RAILWAY_URL")
PORT = int(os.getenv("PORT", 8080))

if not TELEGRAM_TOKEN or not OPENAI_API_KEY or not RAILWAY_URL:
    raise SystemExit("❌ Environment dəyişənləri çatışmır: TELEGRAM_BOT_TOKEN, OPENAI_API_KEY, RAILWAY_URL")

openai.api_key = OPENAI_API_KEY

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Salam! Mən GPT-4 əsaslı Telegram botuyam. Mesaj yaz, cavab al!")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Yazmaq istədiyini mənə göndər, mən GPT-4 ilə cavab verim ✨")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": user_text}]
        )
        gpt_reply = response.choices[0].message.content
    except Exception as e:
        gpt_reply = f"❌ GPT-4 cavab verərkən xəta baş verdi: {e}"
    await update.message.reply_text(gpt_reply)

if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    webhook_url = f"{RAILWAY_URL}/{TELEGRAM_TOKEN}"
    logging.info(f"🚀 Bot başlayır: {webhook_url}")
    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        webhook_url=webhook_url
    )
