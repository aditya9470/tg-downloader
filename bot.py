import logging
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from yt_dlp import YoutubeDL

# Logging setup
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Start command
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Hello! Main ek Video Downloader bot hoon.\n\n"
        "Mujhe kisi bhi YouTube ya Instagram video ka link bhejiye, main use download karke aapko bhej dunga!"
    )

# Video download aur send karne ka logic
async def handle_video_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    
    # Check agar link sahi hai
    if not (url.startswith("http://") or url.startswith("https://")):
        await update.message.reply_text("❌ Kripya ek sahi video link bhejiye (HTTP/HTTPS).")
        return

    status_message = await update.message.reply_text("⏳ Video process ho rahi hai... Kripya thoda intezar karein.")

    # yt-dlp settings (Video ko temporary download karne ke liye)
    ydl_opts = {
        'format': 'best[ext=mp4]/best',  # Sabse acchi MP4 quality
        'outtmpl': 'downloaded_video.%(ext)s', # Temporary file name
        'max_filesize': 45 * 1024 * 1024, # Telegram free bot limit 50MB hoti hai
    }

    try:
        # Video download karein server par
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        # Telegram par user ko video bhejein
        await status_message.edit_text("🚀 Uploading video to Telegram...")
        with open(filename, 'rb') as video_file:
            await update.message.reply_video(video=video_file, caption="✨ Aapki video taiyaar hai! Niche diye arrow par click karke phone me save karein.")
        
        # Kaam khatam hone ke baad server se file delete karein taaki space full na ho
        os.remove(filename)
        await status_message.delete()

    except Exception as e:
        logging.error(f"Error: {e}")
        await status_message.edit_text("❌ Sorry! Ye video download nahi ho payi. Link check karein ya koi dusra link try karein.")
        if os.path.exists('downloaded_video.mp4'):
            os.remove('downloaded_video.mp4')

def main():
    # ⚠️ Yahan apna asli Bot Token dalein
    TOKEN = '8636575145:AAG2PE34kmo-Z4cvRdKpOmxbeZiJUwvgmDE'
    
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_video_link))
    
    print("Bot is starting up...")
    app.run_polling()

if __name__ == '__main__':
    main()
          
