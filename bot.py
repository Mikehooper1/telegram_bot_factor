import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler, MessageHandler, filters, ConversationHandler
import tweepy
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
import yt_dlp
import tempfile

ASK_URL = 1
TELEGRAM_MAX_FILESIZE = 50 * 1024 * 1024  # 50MB

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello! Send /getvideos to fetch videos from a website you choose.')

async def getvideos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Please enter the URL of the website you want to fetch videos from:')
    return ASK_URL

async def fetch_videos_from_url(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    await update.message.reply_text(f'Fetching videos from: {url}')
    try:
        response = requests.get(url, timeout=20)
        soup = BeautifulSoup(response.text, 'html.parser')
        video_links = set()
        # Find <video> tags
        for video in soup.find_all('video'):
            src = video.get('src')
            if src:
                video_links.add(requests.compat.urljoin(url, src))
            for source in video.find_all('source'):
                src = source.get('src')
                if src:
                    video_links.add(requests.compat.urljoin(url, src))
        # Find embedded YouTube/Vimeo links
        for iframe in soup.find_all('iframe'):
            src = iframe.get('src')
            if src and ("youtube.com" in src or "youtu.be" in src or "vimeo.com" in src):
                video_links.add(src)
        if not video_links:
            await update.message.reply_text('No videos found on this page.')
            return ConversationHandler.END
        for link in video_links:
            try:
                if any(domain in link for domain in ["youtube.com", "youtu.be", "vimeo.com"]):
                    # Use yt-dlp for YouTube/Vimeo
                    await update.message.reply_text(f'Downloading from: {link}')
                    with tempfile.TemporaryDirectory() as tmpdir:
                        ydl_opts = {
                            'outtmpl': os.path.join(tmpdir, '%(title)s.%(ext)s'),
                            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4',
                            'max_filesize': TELEGRAM_MAX_FILESIZE,
                            'noplaylist': True,
                        }
                        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                            info = ydl.extract_info(link, download=True)
                            filename = ydl.prepare_filename(info)
                        if os.path.getsize(filename) > TELEGRAM_MAX_FILESIZE:
                            await update.message.reply_text('Video is too large to send via Telegram (50MB limit).')
                        else:
                            with open(filename, 'rb') as f:
                                await update.message.reply_video(video=f)
                else:
                    # Direct video file
                    await update.message.reply_text(f'Downloading direct video: {link}')
                    r = requests.get(link, stream=True, timeout=20)
                    r.raise_for_status()
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmpfile:
                        for chunk in r.iter_content(chunk_size=8192):
                            tmpfile.write(chunk)
                        tmpfile.flush()
                        size = os.path.getsize(tmpfile.name)
                        if size > TELEGRAM_MAX_FILESIZE:
                            await update.message.reply_text('Video is too large to send via Telegram (50MB limit).')
                        else:
                            with open(tmpfile.name, 'rb') as f:
                                await update.message.reply_video(video=f)
                    os.unlink(tmpfile.name)
            except Exception as e:
                await update.message.reply_text(f'Error downloading/sending video: {e}')
    except Exception as e:
        await update.message.reply_text(f'Error fetching videos: {e}')
    return ConversationHandler.END

def main():
    print("Bot is starting...")
    load_dotenv()
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    if not token:
        print("Error: TELEGRAM_BOT_TOKEN is missing or empty in your .env file.")
        return
    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler('start', start))
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('getvideos', getvideos)],
        states={
            ASK_URL: [MessageHandler(filters.TEXT & ~filters.COMMAND, fetch_videos_from_url)]
        },
        fallbacks=[]
    )
    app.add_handler(conv_handler)
    app.run_polling()

if __name__ == '__main__':
    main() 