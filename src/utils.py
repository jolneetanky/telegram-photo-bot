from telegram import Message
from custom_types import MediaFile
import os

"""
This function returns the list of media files for a given message.
If the message is not part of an album, returns just the file of that message itself.
Else, it returns all other files in that album (at least those stored in memory).
"""
def get_media_files(msg: Message, context) -> list[MediaFile]:
    if not msg or not msg.photo:
        raise Exception("Please use this command as a reply to an album or image.")

    media_group_to_msg_map = context.application.bot_data["media_group_to_msg_map"]
    media_group_id = str(msg.media_group_id)
    download_folder = context.application.bot_data["server_download_folder"] # folder to download images onto server

    # some pictures (that don't belong to an album) have no media_group_id.
    messages = [msg]
    # messages = [] # messages whose photo we wna upload
    if media_group_id:
        media_group_to_msg_map[media_group_id].add(msg) # add just in case maybe the server restarted or something, and this file is gone from mem
        messages = list(media_group_to_msg_map[media_group_id])
    
    media_files = []
    for msg in messages:
        photo = msg.photo[-1]
        media_files.append(MediaFile(photo.file_id, photo.file_id, f"{download_folder}/{photo.file_id}"))
    
    # media_files = list(map(lambda m: (m.photo[-1].file_id, m.photo[-1].file_id, f"{download_folder}/{m.photo[-1].file_id}.jpg"), media_files))
    return media_files

"""
Deletes a file from server.
"""
def delete_file(file: MediaFile) -> None:
    try:
        if os.path.exists(file.server_download_path):
            os.remove(file.server_download_path)
    except Exception as e:
        print(f"[delete_file()] Failed to delete {file.server_download_path}: {e}")