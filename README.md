# Telegram Video Download Bot with Automatic Proxy Management

This Telegram bot can download videos from websites and automatically manages proxies to bypass geo-restrictions and access blocked content.

## Features

- **Automatic Proxy Management**: Automatically finds, tests, and rotates working proxies
- **Video Download**: Downloads videos from websites, YouTube, Vimeo, and direct video links
- **Proxy Rotation**: Automatically switches to working proxies when one fails
- **Background Updates**: Continuously updates the proxy list every 5 minutes
- **Telegram Integration**: Sends downloaded videos directly to Telegram

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Environment Configuration

Create a `.env` file in your project directory:

```env
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
```

To get a Telegram bot token:
1. Message [@BotFather](https://t.me/botfather) on Telegram
2. Send `/newbot`
3. Follow the instructions to create your bot
4. Copy the token to your `.env` file

### 3. Run the Bot

```bash
python bot.py
```

## How It Works

### Automatic Proxy Management

The bot uses `proxy_manager.py` to:

1. **Fetch Proxies**: Automatically fetches free proxies from multiple sources
2. **Test Proxies**: Tests each proxy for functionality
3. **Rotate Proxies**: Automatically switches to working proxies
4. **Handle Failures**: Marks failed proxies and switches to alternatives
5. **Background Updates**: Updates the proxy list every 5 minutes

### Proxy Sources

The bot fetches proxies from:
- GitHub repositories with proxy lists
- Public proxy aggregators
- Multiple sources for redundancy

### Usage

1. Start the bot with `/start`
2. Send `/getvideos` to begin
3. Enter the URL of the website containing videos
4. The bot will:
   - Fetch the webpage using a working proxy
   - Find all video links
   - Download and send videos via Telegram
   - Automatically handle proxy failures

## Files

- `bot.py` - Main Telegram bot with proxy integration
- `proxy_manager.py` - Automatic proxy management system
- `test_proxy.py` - Test script for proxy functionality
- `requirements.txt` - Python dependencies
- `.env` - Environment variables (create this)

## Testing

Test the proxy manager:

```bash
python test_proxy.py
```

This will:
- Fetch and test proxies
- Verify proxy rotation
- Test failure handling
- Run auto-update for 10 seconds

## Proxy Configuration

### Manual Proxy (Optional)

If you want to use a specific proxy instead of automatic management, add to your `.env`:

```env
PROXY_URL=http://your-proxy-server:port
```

### Proxy Authentication

For proxies requiring authentication:

```env
PROXY_URL=http://username:password@proxy-server:port
```

## Troubleshooting

### No Working Proxies

If no proxies are found:
1. Check your internet connection
2. The proxy sources might be temporarily unavailable
3. Try running the test script to debug

### Proxy Failures

The bot automatically handles proxy failures by:
1. Marking failed proxies
2. Rotating to working alternatives
3. Retrying downloads with new proxies

### Large Videos

Videos larger than 50MB cannot be sent via Telegram. The bot will notify you if a video is too large.

## Security Notes

- Free proxies may log your traffic
- Use paid proxies for sensitive content
- The bot only uses HTTP/HTTPS proxies, not SOCKS

## Limitations

- Works on PythonAnywhere (proxy only, no VPN)
- Requires working proxies for geo-restricted content
- 50MB Telegram file size limit
- Free proxies may be unreliable

## Support

If you encounter issues:
1. Run `python test_proxy.py` to test proxy functionality
2. Check the console output for error messages
3. Ensure your `.env` file is properly configured 