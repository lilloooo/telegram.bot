from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import os
import logging

# Configurazione del logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# ID del canale, del gruppo e dell'amministratore
CHANNEL_ID = -1002173295724  # ID del canale
GROUP_ID = -1002423029717     # ID del gruppo
ADMIN_ID = 7386325825         # ID dell'amministratore

# Funzione per il comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Ciao! Invia un'immagine o un video e lo riposterò nel canale e nel gruppo. "
    )

# Funzione per notificare l'amministratore in caso di errore
async def notify_admin(error_message: str):
    # Notifica l'amministratore dell'errore
    await context.bot.send_message(chat_id=ADMIN_ID, text=error_message)

# Funzione per inoltrare le immagini
async def repost_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if update.message.photo:
            caption = update.message.caption or "📸 Foto condivisa! 📸"

            # Invia la foto al canale
            await context.bot.send_photo(
                chat_id=CHANNEL_ID,
                photo=update.message.photo[-1].file_id,
                caption=caption
            )
            # Invia la foto al gruppo
            await context.bot.send_photo(
                chat_id=GROUP_ID,
                photo=update.message.photo[-1].file_id,
                caption=caption
            )
            await update.message.reply_text("✅ Foto inviata al canale e al gruppo! ✅")
    except Exception as e:
        await notify_admin(f"Errore nell'invio di una foto: {e}")
        await update.message.reply_text("⚠️ Si è verificato un errore durante l'invio della foto. ⚠️")

# Funzione per inoltrare i video
async def repost_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if update.message.video:
            caption = update.message.caption or "🎥 Video condiviso! 🎥"

            # Invia il video al canale
            await context.bot.send_video(
                chat_id=CHANNEL_ID,
                video=update.message.video.file_id,
                caption=caption
            )
            # Invia il video al gruppo
            await context.bot.send_video(
                chat_id=GROUP_ID,
                video=update.message.video.file_id,
                caption=caption
            )
            await update.message.reply_text("✅ Video inviato al canale e al gruppo! ✅")
    except Exception as e:
        await notify_admin(f"Errore nell'invio di un video: {e}")
        await update.message.reply_text("⚠️ Si è verificato un errore durante l'invio del video. ⚠️")

# Funzione per gestire altri tipi di file
async def handle_other_files(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📄 Hai inviato un file non supportato. Puoi inviare solo immagini o video. 📄")

# Funzione per il comando /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "📋 Ecco come posso aiutarti:\n"
        "- Invia un'immagine per condividerla nel canale e nel gruppo.\n"
        "- Invia un video per condividerlo nel canale e nel gruppo.\n"
        "- Altri file non sono supportati al momento.\n"
        "- Usa /start per ricevere un messaggio di benvenuto."
    )
    await update.message.reply_text(help_text)

# Configurazione del bot
if __name__ == "__main__":
    token = "7963667330:AAFra_92QqQwnzy4wm2xyZ-6iPBPcj3ML0w"  # Token del bot
    app = ApplicationBuilder().token(token).build()

    # Handler per il comando /start
    app.add_handler(CommandHandler("start", start))

    # Handler per il comando /help
    app.add_handler(CommandHandler("help", help_command))

    # Handler per i messaggi con foto
    app.add_handler(MessageHandler(filters.PHOTO, repost_image))

    # Handler per i messaggi con video
    app.add_handler(MessageHandler(filters.VIDEO, repost_video))

    # Handler per tutti gli altri file
    app.add_handler(MessageHandler(filters.Document.ALL, handle_other_files))

    # Avvio del bot
    logging.info("Avvio del bot...")
    app.run_polling()
