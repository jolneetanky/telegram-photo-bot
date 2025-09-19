from telegram import Update
from telegram.ext import ContextTypes
from src.gdrive.gdrive_folder import GDriveFolder
from src.tele_utils import tele_utils
from src.gdrive.gdrive_folder import GDriveFolder
from src.exceptions import GDriveLinkNotSetError, CaptionIsNotCommandError, InvalidFolderPathArgError

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

    chat = update.message.chat

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
        await update.message.reply_text('Invalid folder name. Send /help for how to format folder names.')
        return

    # 2) Upload images in `target_msg` to drive.
    try:
        await tele_utils.upload_to_drive(target_msg, context, folders, gdrive_root_folder)
        await update.message.reply_text(f"Successfully uploaded to gdrive at {tele_utils.get_root_gdrive_folder(chat, context).link}!")

        # NOTE: for now, we just delete from cache
        tele_utils.update_cache(target_msg, context)
    except Exception as e:
        print("[upload()] Failed to upload images: ", e)
        await update.message.reply_text("An error occurred. Please try again.")

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

    folders = []
    target_msg = update.message # message containing the photo
    try:
        folders = tele_utils.extract_caption_folder_components(target_msg.caption)
    except CaptionIsNotCommandError:
        print("CAPTION IS NOT COMMAND")
        return # we don't want this function to do anything cause our caption is not a command.
    except InvalidFolderPathArgError as e:
        await update.message.reply_text(e.message)
        return
    except Exception as e:
        print("Failed to extract caption folder components:", e)
        await update.message.reply_text('Invalid folder name. Send /help for how to format folder names.')
        return
    
    print("FOLDERS:", folders)

    # get gdrive root folder
    gdrive_root_folder = None
    try:
        gdrive_root_folder: GDriveFolder = tele_utils.get_root_gdrive_folder(target_msg.chat, context)
    except GDriveLinkNotSetError:
        await update.message.reply_text("Please set a GDrive folder link, via /set_link <link>.")
        return

    try:
        await tele_utils.upload_to_drive(target_msg, context, folders, gdrive_root_folder)
        await update.message.reply_text(f"Successfully uploaded to gdrive at {tele_utils.get_root_gdrive_folder(target_msg.chat, context).link}!")
        tele_utils.update_cache(target_msg, context)
    except Exception as e:
        print("[upload()] Failed to upload images: ", e)
        await update.message.reply_text("An error occurred. Please try again.")

async def help_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = """
*__🟢 TO START:__*

`/set_link <link>`

\- *sets the Google Drive folder link you'd like to upload your photos to*\. 

\- Subsequent uploads in this chat will be made to the specified folder\.

\- *_You can always reset the link anytime\._*

*__☁️ UPLOADING A PHOTO/ALBUM__*

1\. To upload a photo/album, simply *send your photos here in the chat\.*

2\. *__Either:__*
a\) _Directly send_ command `/upload` *in the caption*\. OR
b\) _Reply to the message_ with the command `/upload`\.

3\. If you want to specify a custom folder to upload to \(*within the folder you set*\), refer below\.

>*NOTE:* 
>Once you upload an album, trying to upload it again \(eg\. by replying to it\) will only upload ONE photo \(the last photo\) in the album\. WIP to fix this\.

*__📂 SPECIFYING CUSTOM FOLDER PATHS__*

1\. *__Nested Paths__*

Just add a spacing in between each path\. 

>*__EXAMPLE__:*
>
>`/upload folder1 folder2`
>
>is equivalent to
>
>`/upload https://drive.google.com/1234/folder1/folder2`\.||

2\. *__Folder Names with Spacing__*

Simply wrap the name in double quotes\. 

>*__EXAMPLE__:*
>
>`/upload "spacing 1" nospacing "spacing 2"` 
>
>is equivalent to
>
>`/upload https://drive.google.com/1234/"spacing 1"/nospacing/"spacing 2"`\.||

*__👥 USAGE IN GROUP CHATS__*

You can add this bot to any of your group chats\. Usage is exactly is the same as above\.

After setting the GDrive link, subsequent uploads in the group chat will be made to the specified folder\. 

Same as before, *_you can always reset the link anytime\._*
    """
    await update.message.reply_text(help_text, parse_mode="markdownV2")

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

    await update.message.reply_text(f"Set root GDrive folder link of this chat to {folder_link}.")
