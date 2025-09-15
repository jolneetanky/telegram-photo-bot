from telegram.ext import Application, MessageHandler, CommandHandler, filters
from dotenv import load_dotenv
# from gdrive import create_folder_if_not_exists
# from gdrive import upload_file
from gdrive import GDriveService
import os

# write handler to accept the command "post_image"
# async def reply(update, context):
# async def upload_to_gdrive(folder_name: str):
#     gdrive_link = "https://drive.google.com/drive/folders/1nn8WI7Kl4iKTxyPzgi8Z1-W5RagXlMi2"

def get_folder_name():
    return "test"

async def extract_img():
    pass

async def delete_img(imgFile):
    pass

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
async def upload(update, context):
    # read the photo attached
    # first how to upload photo to google
    # extract img
    gdrive_service = context.application.bot_data["gdrive_service"]
    try:
        imgFile = await extract_img() # download file to server

        await update.message.reply_text("uploading to gdrive...")
        # 1) get folder name
        folder_name = get_folder_name()
        gdrive_parent_folder_id = os.getenv("GDRIVE_ROOT_FOLDER_ID") # TODO: maybe can pass in as argument?
        project_root = os.getenv("PROJECT_ROOT_PATH")

        # 2) create folder if not exists
        print("Creating folder if not exists...")
        # create_folder_if_not_exists(folder_name, gdrive_parent_folder_id)
        folder_id = gdrive_service.create_folder_if_not_exists(folder_name, gdrive_parent_folder_id)
        print("Successfully created folder if not exists")

        filePaths = ["/Users/jolene/repos/telegram-photo-bot/images/test.jpg"]

        for filePath in filePaths:
            fileName = "test img"
            print("Uploading file...")
            # gdrive_service.upload_file(filePath, fileName, "image/jpg", folder_id)
            gdrive_service.upload_file(filePath, fileName, "image/jpg", folder_id)
            print("Successfully uploaded file")
        # 3) upload to folder
        await update.message.reply_text("successfully uploaded to gdrive!")

        await delete_img(imgFile) # delete file from server
    except:
        pass

def main():
    # Load environment variables from .env file
    load_dotenv()

    """
    Handles the initial launch of the program (entry point).
    """
    token = os.getenv("TOKEN")
    SCOPES = ['https://www.googleapis.com/auth/drive']
    GDRIVE_ROOT_FOLDER_ID = os.getenv("GDRIVE_ROOT_FOLDER_ID")
    SERVICE_ACCOUNT_FILE = os.getenv("SERVICE_ACCOUNT_FILE")
    PROJECT_ROOT = os.getenv("PROJECT_ROOT_PATH")

    gdrive_service = GDriveService(SCOPES, SERVICE_ACCOUNT_FILE)

    application = Application.builder().token(token).concurrent_updates(True).read_timeout(30).write_timeout(30).build()
    # bot data (shared data)
    application.bot_data["gdrive_service"] = gdrive_service

    # application.add_handler(MessageHandler(filters.TEXT, reply)) # new text handler here
    application.add_handler(CommandHandler("upload", upload)) # new command handler here
    print("Telegram Bot started!", flush=True)

    # bot can be added to a group chat - HOW?
    # within this particular group chat, the bot can take in a command: `set_gdrive_link` to set the link. Future pictures will all be sent to here.
    # then when attachments are sent, after running ``

    # SUPER HARD CODED: we just hardcode the gdrive link
    # add bot to group chat
    # command to post an image: `/post <foldername>`
    # if `<foldername>` not passed in, default argument is just the poster's username.

    application.run_polling()

if __name__ == '__main__':
    main()