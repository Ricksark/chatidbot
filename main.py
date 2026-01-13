import os
import threading
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# --- SECTION 1: The Bot Logic ---

# Function to handle the /start and /id command
async def get_chat_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    chat_type = update.effective_chat.type
    user_first_name = update.effective_user.first_name
    
    response_text = (
        f"👋 Hello {user_first_name}!\n\n"
        f"🆔 **Your Chat ID is:** `{chat_id}`\n"
        f"group type: {chat_type}"
    )
    
    # Send message back (parse_mode='Markdown' allows bolding)
    await update.message.reply_text(response_text, parse_mode='Markdown')

# --- SECTION 2: The Keep-Alive Web Server ---

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is alive!"

def run_web_server():
    # Get the port from the environment variable (required for Render)
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

# --- SECTION 3: Main Execution ---

def main():
    # 1. Get the Token from Environment Variable (Secure way) 
    # OR paste it directly below like: TOKEN = "YOUR_TOKEN_HERE" (Not recommended for public code)
    TOKEN = os.environ.get("8200685670:AAGnyTiuXcjhy-H_VZYXr2bffWP90a8dtmA")

    if not TOKEN:
        print("Error: No Token Found!")
        return

    # 2. Build the Application
    application = Application.builder().token(TOKEN).build()

    # 3. Add Handlers
    application.add_handler(CommandHandler("start", get_chat_id))
    application.add_handler(CommandHandler("id", get_chat_id))

    # 4. Start the Web Server in a separate thread (Non-blocking)
    print("Starting Web Server...")
    server_thread = threading.Thread(target=run_web_server)
    server_thread.start()

    # 5. Start the Bot (Blocking)
    print("Bot is polling...")
    application.run_polling()

if __name__ == '__main__':
    main()
