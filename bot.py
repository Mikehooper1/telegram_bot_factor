import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler, MessageHandler, filters, ConversationHandler
import tweepy
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
import yt_dlp
import tempfile
import re
from urllib.parse import urlparse

ASK_URL = 1
TELEGRAM_MAX_FILESIZE = 50 * 1024 * 1024  # 50MB

# Supported platforms
SUPPORTED_PLATFORMS = {
    'youtube.com': 'YouTube',
    'youtu.be': 'YouTube',
    'youtube.com/shorts': 'YouTube Shorts',
    'instagram.com': 'Instagram',
    'tiktok.com': 'TikTok',
    'vm.tiktok.com': 'TikTok',
    'vimeo.com': 'Vimeo',
    'terabox.com': 'Terabox',
    'teraboxapp.com': 'Terabox',
    'terabox.app': 'Terabox',
    '1024tera.com': 'Terabox',
    '4funbox.com': 'Terabox',
    'mirrobox.com': 'Terabox',
    'momerybox.com': 'Terabox',
    'dropbox.com': 'Dropbox',
    'drive.google.com': 'Google Drive',
    'onedrive.live.com': 'OneDrive',
    'mega.nz': 'MEGA',
    'mediafire.com': 'MediaFire'
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        '🎥 **Video Downloader Bot**\n\n'
        'I can download videos from:\n'
        '• YouTube & YouTube Shorts\n'
        '• Instagram Reels & Posts\n'
        '• TikTok Videos\n'
        '• Vimeo\n'
        '• Cloud Drives (Terabox, Dropbox, Google Drive, etc.)\n'
        '• Direct video links\n\n'
        'Send /getvideos to start downloading!'
    )

async def getvideos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        '📥 **Video Download**\n\n'
        'Please send me the URL of the video you want to download.\n\n'
        'Supported platforms:\n'
        '• Instagram Reels/Posts\n'
        '• YouTube/YouTube Shorts\n'
        '• TikTok\n'
        '• Vimeo\n'
        '• Cloud drives (Terabox, Dropbox, etc.)\n'
        '• Direct video links'
    )
    return ASK_URL

def detect_platform(url):
    """Detect the platform from the URL"""
    parsed = urlparse(url)
    domain = parsed.netloc.lower()
    path = parsed.path.lower()
    
    # Check for specific patterns
    if 'youtube.com/shorts' in url or 'youtu.be' in url:
        return 'YouTube Shorts'
    elif 'instagram.com' in domain:
        return 'Instagram'
    elif 'x.com' in domain:
        return 'X'
    elif 'tiktok.com' in domain or 'vm.tiktok.com' in domain:
        return 'TikTok'
    elif any(terabox_domain in domain for terabox_domain in ['terabox', '1024tera', '4funbox', 'mirrobox', 'momerybox']):
        return 'Terabox'
    elif 'dropbox.com' in domain:
        return 'Dropbox'
    elif 'drive.google.com' in domain:
        return 'Google Drive'
    elif 'onedrive.live.com' in domain:
        return 'OneDrive'
    elif 'mega.nz' in domain:
        return 'MEGA'
    elif 'pornhub.com' in domain or 'xvideos.com' in domain or 'pornhub.org' in domain or 'xvideos.com' in domain  or 'xvideos.com' in domain or 'xvideos.com' in domain or 'pornhub.com' in domain or 'xvideos.com' in domain or 'pornhub.com' in domain or 'xvideos.com' in domain or 'pornhub.com' in domain or 'xvideos.com' in domain or 'pornhub.com' in domain or 'xvideos.com' in domain or 'pornhub.com' in domain or 'xvideos.com' in domain or 'pornhub.com' in domain or 'xvideos.com' in domain or 'pornhub.com' in domain or 'xvideos.com' in domain or 'pornhub.com' in domain or 'xvideos.com' in domain or 'pornhub.com' in domain or 'xvideos.com' in domain or 'pornhub.com' in domain or 'xvideos.com' in domain or 'pornhub.com' in domain or 'xvideos.com' in domain or 'pornhub.com' in domain or 'xvideos.com' in domain or 'pornhub.com' in domain or 'xvideos.com' in domain or 'pornhub.com' in domain or 'xvideos.com' in domain or 'pornhub.com' in domain or 'xvideos.com' in domain or 'pornhub.com' in domain or 'xvideos.com' in domain or 'pornhub.com' in domain or 'xvideos.com' in domain or 'pornhub.com' in domain or 'xvideos.com' in domain or 'pornhub.com' in domain or 'xvideos.com' in domain or 'pornhub.com' in domain or 'xvideos.com' in domain or 'pornhub.com' in domain or 'xvideos.com' in domain or 'pornhub.com' in domain or 'xvideos.com' in domain or 'pornhub.com' in domain or 'xvideos.com' in domain or 'pornhub.com' in domain or 'xvideos.com' in domain or 'pornhub.com' in domain or 'xvideos.com' in domain or 'pornhub.com' in domain or 'xvideos.com' in domain or 'pornhub.com' in domain or 'xvideos.com' in domain or 'pornhub.com' in domain or 'xvideos.com' in domain or 'pornhub.com' in domain or 'xvideos.com' in domain or 'pornhub.com' in domain or 'xvideos.com' in domain or 'pornhub.com' in domain or 'xvideos.com' in domain or 'pornhub.com' in domain or 'xvideos.com' in domain or 'pornhub.com' in domain or 'xvideos.com' in domain or 'pornhub.com' in domain or 'xvideos.com' in domain or 'pornhub.com' in domain or 'xvideos.com' in domain or 'pornhub.com' in domain or 'xvideos.com' in domain or 'pornhub.com' in domain or 'xvideos.com' in domain or 'pornhub.com' in domain or 'xvideos.com' in domain or 'pornhub.com' in domain or 'xvideos.com' in domain or 'pornhub.com' in domain or 'xvideos.com' in domain or 'pornhub.com' in domain or 'xvideos.com' in domain or 'pornhub.com' in domain or 'xvideos.com' in domain  or 'xvideos.com' in domain  or 'xvideos.com' in domain  or 'xvideos.com' in domain :
        return 'PornHub'
    elif 'mediafire.com' in domain:
        return 'MediaFire'
    elif 'vimeo.com' in domain:
        return 'Vimeo'
    elif 'youtube.com' in domain:
        return 'YouTube'
    
    return 'Direct Video'

async def fetch_videos_from_url(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    platform = detect_platform(url)
    
    await update.message.reply_text(f'🔍 Detected platform: **{platform}**\n📥 Fetching video from: {url}')
    
    try:
        # Handle different platforms
        if platform in ['YouTube', 'YouTube Shorts', 'Instagram', 'TikTok', 'Vimeo']:
            await download_with_ytdlp(update, url, platform)
        elif platform in ['Terabox', 'Dropbox', 'Google Drive', 'OneDrive', 'MEGA', 'MediaFire']:
            await download_cloud_drive(update, url, platform)
        else:
            # Try to extract videos from webpage or direct link
            await extract_videos_from_webpage(update, url)
            
    except Exception as e:
        await update.message.reply_text(f'❌ Error downloading video: {str(e)}')
    
    return ConversationHandler.END

async def download_with_ytdlp(update: Update, url: str, platform: str):
    """Download videos using yt-dlp for supported platforms"""
    try:
        await update.message.reply_text(f'⏳ Downloading from {platform}...')
        
        with tempfile.TemporaryDirectory() as tmpdir:
            ydl_opts = {
                'outtmpl': os.path.join(tmpdir, '%(title)s.%(ext)s'),
                'format': 'best[filesize<50M]/best[height<=720]/best',
                'max_filesize': TELEGRAM_MAX_FILESIZE,
                'noplaylist': True,
                'quiet': True,
                'no_warnings': True,
                'extract_flat': False,
            }
            
            # Platform-specific options
            if platform == 'Instagram':
                ydl_opts['format'] = 'best[filesize<50M]/best[height<=720]/best'
            elif platform == 'TikTok':
                ydl_opts['format'] = 'best[filesize<50M]/best'
            elif platform in ['YouTube', 'YouTube Shorts']:
                ydl_opts['format'] = 'bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/best[height<=720]/best'
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # Extract info first
                info = ydl.extract_info(url, download=False)
                title = info.get('title', 'Unknown Title')
                
                await update.message.reply_text(f'📹 **{title}**\n⏳ Downloading...')
                
                # Download the video
                ydl.download([url])
                
                # Find the downloaded file
                downloaded_files = [f for f in os.listdir(tmpdir) if os.path.isfile(os.path.join(tmpdir, f))]
                
                if downloaded_files:
                    file_path = os.path.join(tmpdir, downloaded_files[0])
                    file_size = os.path.getsize(file_path)
                    
                    if file_size > TELEGRAM_MAX_FILESIZE:
                        await update.message.reply_text(
                            f'⚠️ Video is too large ({file_size // (1024*1024)}MB) for Telegram (50MB limit).\n'
                            f'Try a shorter video or different format.'
                        )
                    else:
                        await update.message.reply_text('✅ Uploading to Telegram...')
                        with open(file_path, 'rb') as f:
                            await update.message.reply_video(
                                video=f,
                                caption=f'📹 {title}\n📱 Downloaded from {platform}',
                                supports_streaming=True
                            )
                        await update.message.reply_text('✅ Video uploaded successfully!')
                else:
                    await update.message.reply_text('❌ No video file found after download.')
                    
    except yt_dlp.utils.DownloadError as e:
        await update.message.reply_text(f'❌ Download error: {str(e)}')
    except Exception as e:
        await update.message.reply_text(f'❌ Unexpected error: {str(e)}')

async def download_cloud_drive(update: Update, url: str, platform: str):
    """Handle cloud drive downloads"""
    try:
        await update.message.reply_text(f'☁️ Processing {platform} link...')
        
        # Special handling for Terabox sharing links
        if platform == 'Terabox':
            await update.message.reply_text('📋 Terabox sharing link detected. Processing...')
            
            # Try to extract direct download link from Terabox sharing page
            try:
                response = requests.get(url, timeout=30, headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                })
                
                if response.status_code == 200:
                    # Try yt-dlp first (it has built-in Terabox support)
                    try:
                        await download_with_ytdlp(update, url, platform)
                        return
                    except Exception as e:
                        await update.message.reply_text(f'⚠️ yt-dlp failed: {str(e)}')
                
                await update.message.reply_text(
                    '⚠️ Terabox sharing link processing failed.\n\n'
                    'Please try:\n'
                    '1. Make sure the link is public and accessible\n'
                    '2. Try getting a direct download link from Terabox\n'
                    '3. Check if the file is still available'
                )
                
            except Exception as e:
                await update.message.reply_text(f'❌ Error processing Terabox link: {str(e)}')
        
        # For other cloud drives, try yt-dlp first
        else:
            try:
                await download_with_ytdlp(update, url, platform)
            except Exception as e:
                await update.message.reply_text(
                    f'⚠️ Direct download not supported for {platform}.\n'
                    f'Error: {str(e)}\n\n'
                    'Please provide a direct download link.'
                )
            
    except Exception as e:
        await update.message.reply_text(f'❌ Error processing {platform} link: {str(e)}')

async def extract_videos_from_webpage(update: Update, url: str):
    """Extract videos from a webpage"""
    try:
        await update.message.reply_text('🌐 Scanning webpage for videos...')
        
        response = requests.get(url, timeout=20, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
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
        
        # Find embedded video links
        for iframe in soup.find_all('iframe'):
            src = iframe.get('src')
            if src and any(domain in src for domain in ["youtube.com", "youtu.be", "vimeo.com", "instagram.com", "tiktok.com"]):
                video_links.add(src)
        
        # Find video links in href attributes
        for link in soup.find_all('a', href=True):
            href = link.get('href')
            if href and any(ext in href.lower() for ext in ['.mp4', '.avi', '.mov', '.wmv', '.flv', '.webm']):
                video_links.add(requests.compat.urljoin(url, href))
        
        if not video_links:
            await update.message.reply_text('❌ No videos found on this webpage.')
            return
        
        await update.message.reply_text(f'🎥 Found {len(video_links)} video(s) on the webpage.')
        
        for i, link in enumerate(video_links, 1):
            try:
                await update.message.reply_text(f'📥 Downloading video {i}/{len(video_links)}...')
                
                # Try yt-dlp first
                try:
                    await download_with_ytdlp(update, link, 'Direct Video')
                except:
                    # Fallback to direct download
                    await download_direct_video(update, link)
                    
            except Exception as e:
                await update.message.reply_text(f'❌ Error downloading video {i}: {str(e)}')
                
    except Exception as e:
        await update.message.reply_text(f'❌ Error scanning webpage: {str(e)}')

async def download_direct_video(update: Update, url: str):
    """Download direct video files"""
    try:
        r = requests.get(url, stream=True, timeout=30, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        r.raise_for_status()
        
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmpfile:
            total_size = 0
            for chunk in r.iter_content(chunk_size=8192):
                if total_size > TELEGRAM_MAX_FILESIZE:
                    await update.message.reply_text('⚠️ Video is too large for Telegram (50MB limit).')
                    return
                tmpfile.write(chunk)
                total_size += len(chunk)
            
            tmpfile.flush()
            
            if total_size > TELEGRAM_MAX_FILESIZE:
                await update.message.reply_text('⚠️ Video is too large for Telegram (50MB limit).')
            else:
                await update.message.reply_text('✅ Uploading to Telegram...')
                with open(tmpfile.name, 'rb') as f:
                    await update.message.reply_video(
                        video=f,
                        caption='📹 Direct video download',
                        supports_streaming=True
                    )
                await update.message.reply_text('✅ Video uploaded successfully!')
        
        os.unlink(tmpfile.name)
        
    except Exception as e:
        await update.message.reply_text(f'❌ Error downloading direct video: {str(e)}')

def main():
    print("🎥 Video Downloader Bot is starting...")
    load_dotenv()
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    if not token:
        print("❌ Error: TELEGRAM_BOT_TOKEN is missing or empty in your .env file.")
        return
    
    print("✅ Bot token loaded successfully")
    app = ApplicationBuilder().token(token).build()
    
    # Add handlers
    app.add_handler(CommandHandler('start', start))
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('getvideos', getvideos)],
        states={
            ASK_URL: [MessageHandler(filters.TEXT & ~filters.COMMAND, fetch_videos_from_url)]
        },
        fallbacks=[]
    )
    app.add_handler(conv_handler)
    
    print("🚀 Bot is running...")
    app.run_polling()

if __name__ == '__main__':
    main() 