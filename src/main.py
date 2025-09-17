from collections import defaultdict
from telegram import Update, Message
from telegram.ext import Application, MessageHandler, CommandHandler, filters
from dotenv import load_dotenv
from gdrive import GDriveService
import os
from utils import get_media_files, delete_file, get_folder_components

# write handler to accept the command "post_image"
# async def reply(update, context):
# async def upload_to_gdrive(folder_name: str):
#     gdrive_link = "https://drive.google.com/drive/folders/1nn8WI7Kl4iKTxyPzgi8Z1-W5RagXlMi2"

async def delete_img(imgFile):
    pass

async def handle_album(update: Update, context):
    messages = update.message  # actually a list of Message objects
    file_paths = []
    for msg in messages:
        largest_photo = msg.photo[-1]
        file_id = largest_photo.file_id
        file_name = f"{file_id}.jpg"
        path = f"./images/{file_name}"
        file_paths.append((file_id, file_name, path))
    print(file_paths)

# def get_image_file

"""
Given a message, returns all image file names of images in the same album as `message`.
Returns array of tuples: (file_id, file_name, file_path)
"""
def get_album_image_files(message: Message, image_folder_path: str) -> list[tuple[str]]:
    print("[get_image_files()]")

    if not message.photo:
        return []

    file_paths = []

    for photo_size in message.photo:
        file_id = photo_size.file_id
        # download file
        file_name = f"{file_id}.jpg"
        path = f"{image_folder_path}/{file_id}.jpg"
        file_paths.append((file_id, file_name, path))

    return file_paths

#photo=(PhotoSize(file_id='AgACAgUAAyEFAASUN-rnAAIBCmjJAta4ZmeW9eV5BJYKGf9Yy55oAAKWyzEbDeJIVsa_b2rRUlvLAQADAgADcwADNgQ', file_size=1189, file_unique_id='AQADlssxGw3iSFZ4', height=90, width=40)
# image_folder_path DOES NOT end with a "/".
"""
Downloadsd an image from telegram to server.
"""
async def extract_and_download_image(context, image_folder_path: str, file_id: str, download_path: str) -> None:
    print("[extract_and_download_image()]")

    try:
        # create directory first
        os.makedirs(image_folder_path, exist_ok = True)
        file = await context.bot.get_file(file_id)
        await file.download_to_drive(download_path)

    except Exception as e:
        print("[extract_and_download_images()] Failed to download image: ", e)
        raise e

"""
Context {
    application: {
        bot_data: {
            gdrive_service: GDriveService,
            project_root: str,
        }
    }
}
"""
# TODO: from the album,
# extract images
# and install into server.
async def upload_handler(update: Update, context):
    gdrive_service = context.application.bot_data["gdrive_service"]
    download_folder = context.application.bot_data["server_download_folder"] # folder to download images onto server
    gdrive_parent_folder_id = os.getenv("GDRIVE_ROOT_FOLDER_ID") # TODO: maybe can pass in as argument?

    target_msg = update.message.reply_to_message
    # return if message is not a reply, or message does not contain a photo
    if not target_msg or not target_msg.photo:
        await update.message.reply_text("Please use this command as a reply to an album or image.")
        return
    
    # 1) get gdrive folder name
    try:
        print("there0")
        paths = get_folder_components(update, context)
        print("there1")
        print("PATHS: ", paths)
        folder_name = paths[0]
    except Exception as e:
        print("Failed to get folder name:", e)
        await update.message.reply_text('Invalid folder name. If you want a folder name with spacing, remember to start and end with double quotes (Eg. "My Folder").')
        return

    created_files = []

    await update.message.reply_text(f"Uploading to gdrive to folder {folder_name}...")
    
    try:
        # 2) create folder if not exists
        folder_id = gdrive_service.create_folder_if_not_exists(folder_name, gdrive_parent_folder_id)
        print(f"[upload_handler()] Successfully created folder {folder_name} if not exists")

        # for each file, download to server, then upload to gdrive
        media_files = get_media_files(target_msg, context)
        for i in range(len(media_files)):
            file = media_files[i]
            await update.message.reply_text(f"Uploading {i+1}/{len(media_files)}... ")

            print("[upload_handler()] Downloading file...")
            await extract_and_download_image(context, download_folder, file.id, file.server_download_path)
            print("[upload_handler()] Successfully downloaded file")

            print("[upload_handler()] Uploading file...")
            gdrive_service.upload_file(file.server_download_path, file.name, "image/jpg", folder_id)
            print("[upload_handler()] Successfully uploaded file")

            created_files.append(file)

        await update.message.reply_text("Successfully uploaded to gdrive!")

        # await delete_img(imgFile) # delete file from server
    except Exception as e:
        print("[upload()] Failed to upload images: ", e)
        await update.message.reply_text("An error occurred. Please try again.")

    finally:
        print("[upload_handler()] Deleting files...")
        for file in created_files:
            delete_file(file)
        print("[upload_handler()] Successfully deleted files")

async def start(update: Update, context):
    await update.message.reply_text("Send me a photo, or photos!")

async def handle_media_album(update: Update, context):
    print("[handle_media_album()]")
    message = update.effective_message
    mp = context.application.bot_data["media_group_to_msg_map"]
    if message.media_group_id:
        # this message is part of an album
        mp[message.media_group_id].add(message)

def main():
    # Load environment variables from .env file
    load_dotenv()

    """
    Handles the initial launch of the program (entry point).
    """
    token = os.getenv("BOT_TOKEN")
    SCOPES = ['https://www.googleapis.com/auth/drive']
    # GDRIVE_ROOT_FOLDER_ID = os.getenv("GDRIVE_ROOT_FOLDER_ID")
    SERVICE_ACCOUNT_FILE = os.getenv("SERVICE_ACCOUNT_FILE")
    SERVER_DOWNLOAD_PATH = os.getenv("SERVER_DOWNLOAD_PATH")

    gdrive_service = GDriveService(SCOPES, SERVICE_ACCOUNT_FILE)

    application = Application.builder().token(token).concurrent_updates(True).read_timeout(30).write_timeout(30).build()
    # bot data (shared data)
    application.bot_data["gdrive_service"] = gdrive_service
    application.bot_data["media_group_to_msg_map"] = defaultdict(set)
    application.bot_data["server_download_folder"] = SERVER_DOWNLOAD_PATH

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("upload", upload_handler)) # new command handler here
    application.add_handler(MessageHandler(filters.PHOTO, handle_media_album))
    print("Telegram Bot started!", flush=True)

    application.run_polling()

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print("Error in main():", e)