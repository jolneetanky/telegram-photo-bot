from telegram import Update
from telegram.ext import ContextTypes

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
