from telegram import Message, Update, Chat
from telegram.ext import ContextTypes
from custom_types import MediaFile
from exceptions import GDriveLinkNotSetError
from gdrive.gdrive_folder import GDriveFolder
import os

class TeleUtils:
    """
    Download an image from telegram to server.
    """
    async def download_image_to_server(context: ContextTypes.DEFAULT_TYPE, image_folder_path: str, file_id: str, download_path: str) -> None:
        print("[download_image()]")

        try:
            # create directory first
            os.makedirs(image_folder_path, exist_ok = True)
            file = await context.bot.get_file(file_id)
            await file.download_to_drive(download_path)

        except Exception as e:
            print("[download_image()] Failed to download image: ", e)
            raise e

    """
    This function returns the list of media files for a given message.
    If the message is not part of an album, returns just the file of that message itself.
    Else, it returns all other files in that album (at least those stored in memory).
    """
    def get_media_files_from_message(msg: Message, context) -> list[MediaFile]:
        if not msg or not msg.photo:
            raise Exception("Please use this command as a reply to an album or image.")

        media_group_to_msg_map = context.application.bot_data["media_group_to_msg_map"]
        print("HIII", msg.media_group_id, media_group_to_msg_map)
        media_group_id = str(msg.media_group_id)
        download_folder = context.application.bot_data["server_download_folder"] # folder to download images onto server

        messages = [msg] # messages whose photo who wna upload
        if media_group_id and media_group_id != "None":
            media_group_to_msg_map[media_group_id].add(msg) # add just in case maybe the server restarted or something, and this file is gone from mem
            messages = list(media_group_to_msg_map[media_group_id])
        
        media_files = []
        for msg in messages:
            photo = msg.photo[-1]
            media_files.append(MediaFile(photo.file_id, photo.file_id, f"{download_folder}/{photo.file_id}"))
        
        # media_files = list(map(lambda m: (m.photo[-1].file_id, m.photo[-1].file_id, f"{download_folder}/{m.photo[-1].file_id}.jpg"), media_files))
        return media_files

    """
    Gets folder name based on arguments and stuff
    Raises exception if syntax is not correct.

    Invariants:
    - Cannot have " in the middle of a word.
    - Whenever there is a starting ", there must be an ending " (be it in the same or different word).
    - Whenever there is an ending ", there must be a starting " to match (be it in the same or different word).

    TEST CASES TO TRY:
    # no argument -> [{username}] returned
    # "john" -> valid, parsed as ["john"]
    # "John Doe" mary jane -> valid
    # John "doe mary" jane -> valid, parsed as [John, doe mary, jane]
    # jon doe "mary" jane -> valid, parsed as [jon doe, mary, jane]
    # "John Doe" mary jane" -> invalid, unmatching "
    # john "doe mary jane -> invalid, unmatching "
    # jo"n doe -> invalid, can't have " in between if it's not at the start

    Examples of accepted syntax and how it is parsed:
    1. "John Doe" -> [John Doe]
    2. "John Doe" folder "folder 2" -> [John Doe, folder]
    3. "John" -> [John]

    Examples of invalid syntax:
    1. John Doe - no quotation marks
    2. John Doe" - unmatched quotation mark
    3. "John Doe - unmatched quotation mark
    4. "John Doe"ez nuts - quotation mark in bad position
    """
    def extract_arg_folder_components(update: Update, context) -> list[str]:
        args: list[str] = context.args
        # args = args[0].split("/")

        print("ARGS", args)

        if not args:
            return [update.message.from_user.username]

        paths = [] 
        start_idx = -1 # -1 indicates no current start_idx. If == -1, it means we have no starting " yet.
        i = 0 # this is the current index in `args` we are looking at
        cur_word = []

        while i < len(args):
            # if " in invalid position, raise exception
            for idx in range(len(args[i])):
                if args[i][idx] == '"' and (idx > 0 and idx < len(args[i]) - 1):
                    raise Exception("Quotation in invalid position")
                
            # if standalone quotation, just add the word and continue 
            if args[i].startswith('"') and args[i].endswith('"'):
                cur_word.append(args[i][1:len(args[i]) - 1]) # omit start and end quotation
                paths.append(" ".join(cur_word))
                cur_word = []
                i += 1
                continue

            # ok so now we handle all the other cases
            # ie. 1) quotation mark at start
            # 2) quotation mark at end
            # no quotation marks

            if args[i].startswith('"'):
                if start_idx == -1:
                    start_idx = i
                    cur_word.append(args[i][1:]) # omit the start "
                else:
                    print(f"[get_arg_folder_components()] invalid end quotation")
                    raise Exception("Invalid end quotation")

                i += 1
                continue

            elif args[i].endswith('"'):
                if start_idx == -1:
                    print(f"[get_arg_folder_components()] no matching start quotation")
                    raise Exception("No matching start quotation")
                else:
                    cur_word.append(args[i][:len(args[i]) - 1]) # omit the end "
                    paths.append(" ".join(cur_word))
                    cur_word = []
                    start_idx = -1 # reset start idx

                i += 1
                continue

            # else, no quotations; we can just add into cur_word.
            if start_idx == -1:
                # no start idx, this is a standalone word. Just take it as a path and continue
                paths.append(args[i])
            else:
                cur_word.append(args[i]) # part of an ongoing word, append to `cur_word` and continue

            i += 1

        # at the end, if start_idx != -1 (meaning someone hasn't been completed yet) -> raise exception.
        if start_idx != -1:
            raise Exception("No matching end quotation") 

        return paths

    """
    Gets the root GDrive folder ID of the chat.
    """
    def get_root_gdrive_folder(chat: Chat, context: ContextTypes.DEFAULT_TYPE) -> GDriveFolder:
        mp = context.application.bot_data["chat_to_folder_map"]

        if chat.id not in mp:
            raise GDriveLinkNotSetError
        
        return mp[chat.id]
    
tele_utils = TeleUtils