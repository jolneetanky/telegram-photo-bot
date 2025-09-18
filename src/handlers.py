from telegram import Update
from telegram.ext import ContextTypes
from gdrive import GDriveService
from tele_utils import tele_utils
from utils import pretty_print, is_valid_drive_folder_link, extract_folder_id, delete_file
from exceptions import GDriveLinkNotSetError
import os

"""
This function handles the upload of media to GDrive.
1. Based on the chat type (private/public), the corresponding GDrive root folder is set as the root for all uploads.
2. Extract folder components from arguments.
3. Creates these folders in GDrive (if they don't yet exist).
4. Gets a list of all media files to upload, from the telegram message.
5. For each MediaFile in the list,
    1. Download these files onto the server.
    2. Upload to GDrive, into the leaf folder.
6. Delete the files that were downloaded onto the server. This cleanup happens whether the above ran successfully, and also runs in case of exceptions.
"""
async def upload_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    gdrive_service: GDriveService = context.application.bot_data["gdrive_service"]
    download_folder = context.application.bot_data["server_download_folder"] # folder to download images onto server

    # check if message is a reply to a photo
    target_msg = update.message.reply_to_message
    if not target_msg or not target_msg.photo:
        await update.message.reply_text("Please use this command as a reply to an album or image.")
        return

    # get root folder id based on chat
    chat = update.message.chat
    gdrive_root_folder_id = ""

    try:
        gdrive_root_folder_id = tele_utils.get_root_gdrive_folder_id(chat, context)
    except GDriveLinkNotSetError:
        await update.message.reply_text("Please set a GDrive folder link, via /set_gdrive_link.")
        return

    # except PersonalGDriveLinkNotSetError:
    #     await update.message.reply_text("Please set a personal root GDrive folder link, via /set_gdrive_link_personal.")
    #     return
    # except GroupGDriveLinkNotSetError:
    #     await update.message.reply_text("Please set a root GDrive folder for this group chat, via /set_gdrive_link_group.")
    #     return
    # except Exception as e:
    #     await update.message.reply_text("An unexpected error occured.")
    #     return

    # chat_id = update.message.chat.id
    # chat_type = update.message.chat.type

    # # 1. Get the chat_to_folder_map for the corresponding chat type.
    # if chat_type == "private":
    #     chat_to_folder_map = context.application.bot_data["private_chat_to_folder_map"]
    # else:
    #     chat_to_folder_map = context.application.bot_data["group_chat_to_folder_map"]

    # if chat_id not in chat_to_folder_map:
    #     if chat_type == "private":
    #         await update.message.reply_text("Please set a personal root GDrive folder link, via /set_gdrive_link_personal.")
    #     else:
    #         await update.message.reply_text("Please set a root GDrive folder for this group chat, via /set_gdrive_link_group.")
    #     return

    # 2. Obtain the (set) parent folder ID based on chat ID. 
    # gdrive_parent_folder_id = chat_to_folder_map[chat_id]

    
    # 1) Extract folder components from arguments
    try:
        folders = tele_utils.extract_arg_folder_components(update, context)
    except Exception as e:
        print("Failed to extract arg folder components:", e)
        await update.message.reply_text('Invalid folder name. If you want a folder name with spacing, remember to start and end with double quotes (Eg. "My Folder").')
        return

    created_files = []

    await update.message.reply_text(f"Uploading to gdrive to folder {'/'.join(folders)}...")
    
    try:
        # 2) create folder if not exists
        # folder_id = gdrive_service.create_folder_if_not_exists_prev(folder_name, gdrive_parent_folder_id)
        folder_id = gdrive_service.create_folders_if_not_exists(gdrive_root_folder_id, folders)
        print(f"[upload_handler()] Successfully created folders. Leaf folder ID: {folder_id}")

        # 3) for each file, download to server, then upload to gdrive
        media_files = tele_utils.get_media_files_from_message(target_msg, context)
        for i in range(len(media_files)):
            file = media_files[i]
            await update.message.reply_text(f"Uploading {i+1}/{len(media_files)}... ")

            print("[upload_handler()] Downloading file...")
            await tele_utils.download_image_to_server(context, download_folder, file.id, file.server_download_path)
            print("[upload_handler()] Successfully downloaded file")

            print("[upload_handler()] Uploading file...")
            gdrive_service.upload_file(file.server_download_path, file.name, "image/jpg", folder_id)
            print("[upload_handler()] Successfully uploaded file")

            created_files.append(file)

        await update.message.reply_text("Successfully uploaded to gdrive!")
    except Exception as e:
        print("[upload()] Failed to upload images: ", e)
        await update.message.reply_text("An error occurred. Please try again.")

    finally:
        print("[upload_handler()] Deleting files...")
        for file in created_files:
            delete_file(file)
        print("[upload_handler()] Successfully deleted files")

async def help_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = """
<b>Welcome to tele_photo_bot! 🎉</b>\n
You can use me to upload photos (and videos… but that's a WIP) to Google Drive.\n\n

<b>1.</b> To upload an album, simply <b>send your photos</b> here in this chat.\n
<b>2.</b> Next, <b>reply to the album/photo</b> you want to upload, and send the command: <code>/upload</code>.\n
    This will create a folder with your Telegram username, and the photos will be uploaded there.\n
<b>3.</b> <b>Specifying a folder</b> — if you want to specify a particular folder name, simply do:\n
<code>/upload &lt;folder_name&gt;</code>\n
    (Eg. <code>/upload myfolder</code> → creates the folder titled <code>myfolder</code> in Drive if it doesn't already exist.)\n\n

— If you want the folder name to have spacing (eg. <code>my folder</code>), just include double quotes before and after.\n
    Example: <code>/upload "my folder"</code>\n\n

<b>(SLIGHTLY MORE) ADVANCED FEATURES:</b>\n
<b>UPLOADING FILES TO NESTED FOLDERS:</b>\n
— If you want to upload a file to a nested folder, eg. <code>folder1/folder2/folder3</code>, you need to specify the paths <b>in order</b> like so:\n
<code>/upload folder1 folder2 folder3</code>\n\n

<b>MORE EXAMPLES:</b>\n
— <code>/upload Alice "John Doe" Mary</code> → creates file in folder <code>Alice/"John Doe"/Mary</code>.
"""

    await update.message.reply_text(help_text, parse_mode="HTML")

"""
Sets the gdrive root folder for personal use.
Once set, all requests sent between the user and bot private chat will go to that particular drive.

This command can be send from any type of chat - private or group.
"""
# async def set_root_folder_personal_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     chat = update.message.chat
#     username = update.message.from_user.username

#     args = context.args 
#     # if no argument passed in
#     if not args:
#         await update.message.reply_text("Plase include a Google Drive folder link.")
#         return

#     folder_link = args[0]

#     # if invalid folder link
#     if not is_valid_drive_folder_link(folder_link):
#         await update.message.reply_text("Invalid link format. Please include an actual Google Drive folder link.")
#         return

#     mp = context.application.bot_data["private_chat_to_folder_map"]
#     mp[chat.id] = extract_folder_id(folder_link)

#     await update.message.reply_text(f"Set root GDrive folder link of {username} to {folder_link}.")
    
"""
Sets the gdrive root folder for a group.
Once set, all requests from this group will go to that particular drive.

Edge cases / when exceptions are thrown:
1. User calls this command from within a private chat.
"""
# async def set_root_folder_group_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     chat = update.message.chat
#     # if command sent from private chat with bot
#     if chat.type == "private":
#         await update.message.reply_text("You can only use this command in a group chat.")
#         return

#     args = context.args 
#     # if no argument passed in
#     if not args:
#         await update.message.reply_text("Plase include a Google Drive folder link.")
#         return

#     folder_link = args[0]

#     # if invalid folder link
#     if not is_valid_drive_folder_link(folder_link):
#         await update.message.reply_text("Invalid link format. Please include an actual Google Drive folder link.")
#         return

#     mp = context.application.bot_data["group_chat_to_folder_map"]
#     mp[chat.id] = extract_folder_id(folder_link)

#     await update.message.reply_text(f"Set root GDrive folder link of this group chat to {folder_link}.")

"""
Sets the GDrive link for a particular chat.
Subsequent uploads will go to this GDrive link.
"""
async def set_gdrive_link_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args 
    # if no argument passed in
    if not args:
        await update.message.reply_text("Plase include a Google Drive folder link. Eg. /set_gdrive_link https://drive.google.com/1234)")
        return

    folder_link = args[0]
    chat = update.message.chat

    if not is_valid_drive_folder_link(folder_link):
        await update.message.reply_text("Invalid link format. Please include an actual Google Drive folder link.")
        return

    mp = context.application.bot_data["chat_to_folder_map"]
    mp[chat.id] = extract_folder_id(folder_link)

    await update.message.reply_text(f"Set root GDrive folder link of this chat to {folder_link}.")