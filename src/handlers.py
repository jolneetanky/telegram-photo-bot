from telegram import Update
from telegram.ext import ContextTypes
from gdrive.gdrive_service import GDriveService
from gdrive.gdrive_folder import GDriveFolder
from tele_utils import tele_utils
from utils import delete_file
from gdrive.gdrive_folder import GDriveFolder
from exceptions import GDriveLinkNotSetError

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
    # check if message is a reply to a photo
    target_msg = update.message.reply_to_message
    if not target_msg or not target_msg.photo:
        await update.message.reply_text("Please use this command as a reply to an album or image.")
        return

    # I COPIED FROM THIS POINT ONWARDS
    # get root folder id based on chat
    chat = update.message.chat
    gdrive_service: GDriveService = context.application.bot_data["gdrive_service"]
    download_folder = context.application.bot_data["server_download_folder"] # folder to download images onto server

    try:
        gdrive_root_folder: GDriveFolder = tele_utils.get_root_gdrive_folder(chat, context)
    except GDriveLinkNotSetError:
        await update.message.reply_text("Please set a GDrive folder link, via /set_link <link>.")
        return

    # 1) Extract folder components from arguments
    try:
        folders = tele_utils.extract_arg_folder_components(update, context)
    except Exception as e:
        print("Failed to extract arg folder components:", e)
        await update.message.reply_text('Invalid folder name. If you want a folder name with spacing, remember to start and end with double quotes (Eg. "My Folder").')
        return
    
    '''
    created_files = []

    await update.message.reply_text(f"Uploading to gdrive to folder {'/'.join(folders)}...")
    
    try:
        # 2) create folder if not exists
        # folder_id = gdrive_service.create_folder_if_not_exists_prev(folder_name, gdrive_parent_folder_id)
        folder_id = gdrive_service.create_folders_if_not_exists(gdrive_root_folder.id, folders)
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
        
        await update.message.reply_text(f"Successfully uploaded to gdrive at {tele_utils.get_root_gdrive_folder(chat, context).link}!")
        '''
    try:
        await tele_utils.upload_to_drive(target_msg, context, folders, gdrive_root_folder)
        await update.message.reply_text(f"Successfully uploaded to gdrive at {tele_utils.get_root_gdrive_folder(chat, context).link}!")
    except Exception as e:
        print("[upload()] Failed to upload images: ", e)
        await update.message.reply_text("An error occurred. Please try again.")

    # finally:
    #     print("[upload_handler()] Deleting files...")
    #     for file in created_files:
    #         delete_file(file)
    #     print("[upload_handler()] Successfully deleted files")

"""
When a photo is sent, if it belongs to album, add it to the hashmap `media_group_to_msg_map`.
If there's a caption and the caption starts with "/upload", we're gonna upload it.
"""
async def handle_media_album(update: Update, context):
    print("[handle_media_album()]")
    message = update.effective_message
    mp = context.application.bot_data["media_group_to_msg_map"]
    # TODO: implement cache logic
    # add to hashmap
    if message.media_group_id:
        mp[message.media_group_id].add(message)

    folders = tele_utils.extract_caption_folder_components(update.message.caption)
    if not folders:
        return

    # get gdrive root folder
    gdrive_root_folder = None
    try:
        gdrive_root_folder: GDriveFolder = tele_utils.get_root_gdrive_folder(update.message.chat, context)
    except GDriveLinkNotSetError:
        await update.message.reply_text("Please set a GDrive folder link, via /set_link <link>.")
        return

    try:
        await tele_utils.upload_to_drive(update.message, context, folders, gdrive_root_folder)
        await update.message.reply_text(f"Successfully uploaded to gdrive at {tele_utils.get_root_gdrive_folder(update.message.chat, context).link}!")
    except Exception as e:
        print("[upload()] Failed to upload images: ", e)
        await update.message.reply_text("An error occurred. Please try again.")

async def help_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = """
    *Welcome to tele/_photo/_bot!*

    You can use me to upload photos (and videos… but that's a WIP) to Google Drive.

    *TO START:*
    `/set_link <link>`:
    - *sets the Google Drive folder link you'd like to upload your photos to*. 
    - Subsequent uploads in this chat will be made to the specified folder. Applies to group chats too.

    *UPLOADING A PHOTO/ALBUM*
    1. To upload a photo/album, simply *send your photos here in the chat.*
    2. Next, *reply to the album/photo you want to upload*, and send the command: `/upload`. This will simply upload the files into the folder link you set in `set_link`.
    3. If you want to specify default folders *within the folder you set*, refer below.
    
    *SPECIFYING DEFAULT FOLDER PATHS*
    (*NOTE:* In these examples, `root` refers to the root folder, ie. the one we set using `/set_link`.)
    1. *For nested paths*, just add a spacing in between each path. 
        (Eg. `/upload folder1 folder2` -> `root/folder1/folder2`
    2. *For folder names with spacing*, simply wrap the name in double quotes. 
        (Eg. `/upload "spacing 1" nospacing "spacing 2"` -> `root/"spacing 1"/nospacing/"spacing 2").

"""

    await update.message.reply_text(help_text, parse_mode="markdown")

"""
Sets the GDrive link for a particular chat.
Subsequent uploads will go to this GDrive link.
"""
async def set_gdrive_link_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args 
    # if no argument passed in
    if not args:
        await update.message.reply_text("Plase include a Google Drive folder link. Eg. /set_link https://drive.google.com/1234)")
        return

    folder_link = args[0]
    chat = update.message.chat


    if not GDriveFolder.is_valid_drive_folder_link(folder_link):
        await update.message.reply_text("Invalid link format. Please include an actual Google Drive folder link.")
        return

    mp = context.application.bot_data["chat_to_folder_map"]
    mp[chat.id] = GDriveFolder(folder_link)
    # mp[chat.id] = extract_folder_id(folder_link)

    await update.message.reply_text(f"Set root GDrive folder link of this chat to {folder_link}.")
