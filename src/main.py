from collections import defaultdict
from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, filters
from dotenv import load_dotenv
from gdrive.gdrive_service import GDriveService
from gdrive.gdrive_folder import GDriveFolder
import os
from handlers import help_handler, upload_handler, set_gdrive_link_handler

async def start_handler(update: Update, context):
    await update.message.reply_text("Send me a photo, or photos! If you're unsure how to use this bot, just send /help.")

"""
When a photo is sent, if it belongs to album, add it to the hashmap `media_group_to_msg_map`.
"""
async def handle_media_album(update: Update, context):
    print("[handle_media_album()]")
    message = update.effective_message
    mp = context.application.bot_data["media_group_to_msg_map"]
    if message.media_group_id:
        mp[message.media_group_id].add(message)

def main():
    # Load environment variables from .env file
    load_dotenv()

    """
    Handles the initial launch of the program (entry point).
    """
    token = os.getenv("BOT_TOKEN")
    SCOPES = ['https://www.googleapis.com/auth/drive']
    SERVICE_ACCOUNT_FILE = os.getenv("SERVICE_ACCOUNT_FILE")
    SERVER_DOWNLOAD_PATH = os.getenv("SERVER_DOWNLOAD_PATH")

    gdrive_service = GDriveService(SCOPES, SERVICE_ACCOUNT_FILE)

    application = Application.builder().token(token).concurrent_updates(True).read_timeout(30).write_timeout(30).build()
    # bot data (shared data)
    application.bot_data["gdrive_service"] = gdrive_service
    application.bot_data["media_group_to_msg_map"] = defaultdict(set)
    application.bot_data["server_download_folder"] = SERVER_DOWNLOAD_PATH
    application.bot_data["chat_to_folder_map"] = defaultdict(GDriveFolder) # stores mappings of {chat_id: folder_id}

    application.add_handler(CommandHandler("start", start_handler))
    application.add_handler(CommandHandler("help", help_handler))
    application.add_handler(CommandHandler("set_link", set_gdrive_link_handler))
    application.add_handler(CommandHandler("upload", upload_handler)) # new command handler here
    application.add_handler(MessageHandler(filters.PHOTO, handle_media_album))
    print("Telegram Bot started!", flush=True)

    application.run_polling()

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print("Error in main():", e)