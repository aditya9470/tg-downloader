import logging
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Logging setup
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Start command
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Hello! Main aapka 24x7 Advanced Video Downloader bot hoon.\n\n"
        "Mujhe kisi bhi Instagram Reel ya YouTube video ka link bhejiye, main use download karke bhej dunga!"
    )

# Video download karne ka naya logic (Bypass API Method)
async def handle_video_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    
    if not (url.startswith("http://") or url.startswith("https://")):
        await update.message.reply_text("❌ Kripya ek sahi video link bhejiye.")
        return

    status_message = await update.message.reply_text("⏳ API Se Video Process ho rahi hai... Kripya thoda intezar karein.")

    try:
        # Public Advanced Video Downloader API
        api_url = f"https://api.cobalt.tools/api/json"
        payload = {
            "url": url,
            "vQuality": "720", # standard HD quality
            "isAudioOnly": False
        }
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

        response = requests.post(api_url, json=payload, headers=headers, timeout=15)
        data = response.json()

        if response.status_code == 200 and "url" in data:
            download_link = data["url"]
            await status_message.edit_text("🚀 Uploading video to Telegram...")
            
            # Telegram direct URL se video send kar sakta hai
            await update.message.reply_video(
                video=download_link,
                caption="✨ Aapki video taiyaar hai! Niche diye arrow par click karke phone me save karein."
            )
            await status_message.delete()
        else:
            raise Exception("API status error or link missing")

    except Exception as e:
        logging.error(f"Error: {e}")
        await status_message.edit_text("❌ Sorry! Ye video download nahi ho payi. Link check karein ya thodi der baad try karein.")

def main():
    TOKEN = '8636575145:AAG2PE34kmo-Z4cvRdKpOmxbeZiJUwvgmDE'
    
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_video_link))
    
    print("Bot is starting up with API Mode...")
    app.run_polling()

if __name__ == '__main__':
    main()
