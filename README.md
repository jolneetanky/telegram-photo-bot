# Telegram Photo Bot

## How to use the bot:

1. Add the bot to any channel/group chat you want.
2. Upload photos to the chat as you'd like.
3. When you want to upload a photo to gdrive, just reply to the particular album with the `upload` command, eg: `/upload@tele_photo_bot`
4. The bot will upload photos in that album to gdrive.

## How the bot works:

### 1) Accessing photos in a particular album

When the user replies to an album and sends the `upload` command to the bot, the bot has access to the replied message.

Message is of this shape:

```
{
  "channel_chat_created": false,
  "delete_chat_photo": false,
  "entities": [
    {
      "length": 22,
      "offset": 0,
      "type": "bot_command"
    }
  ],
  "group_chat_created": false,
  "message_thread_id": 265,
  "reply_to_message": {
    "channel_chat_created": false,
    "delete_chat_photo": false,
    "group_chat_created": false,
    "media_group_id": "14064031313798717",
    "photo": [
      {
        "height": 90,
        "width": 40,
        "file_id": "AgACAgUAAyEFAASUN-rnAAIBCmjJAta4ZmeW9eV5BJYKGf9Yy55oAAKWyzEbDeJIVsa_b2rRUlvLAQADAgADcwADNgQ",
        "file_size": 1189,
        "file_unique_id": "AQADlssxGw3iSFZ4"
      },
      {
        "height": 320,
        "width": 144,
        "file_id": "AgACAgUAAyEFAASUN-rnAAIBCmjJAta4ZmeW9eV5BJYKGf9Yy55oAAKWyzEbDeJIVsa_b2rRUlvLAQADAgADbQADNgQ",
        "file_size": 14417,
        "file_unique_id": "AQADlssxGw3iSFZy"
      },
      {
        "height": 800,
        "width": 360,
        "file_id": "AgACAgUAAyEFAASUN-rnAAIBCmjJAta4ZmeW9eV5BJYKGf9Yy55oAAKWyzEbDeJIVsa_b2rRUlvLAQADAgADeAADNgQ",
        "file_size": 58279,
        "file_unique_id": "AQADlssxGw3iSFZ9"
      },
      {
        "height": 1280,
        "width": 576,
        "file_id": "AgACAgUAAyEFAASUN-rnAAIBCmjJAta4ZmeW9eV5BJYKGf9Yy55oAAKWyzEbDeJIVsa_b2rRUlvLAQADAgADeQADNgQ",
        "file_size": 109993,
        "file_unique_id": "AQADlssxGw3iSFZ-"
      }
    ],
    "supergroup_chat_created": false,
    "chat": {
      "id": -1002486692583,
      "is_forum": true,
      "title": "resources for d grind \ud83d\ude2c\ud83d\ude2c",
      "type": "supergroup"
    },
    "date": 1758003914,
    "message_id": 266,
    "from": {
      "first_name": "jolene",
      "id": 1797223820,
      "is_bot": false,
      "language_code": "en",
      "username": "jolneetan"
    }
  },
  "supergroup_chat_created": false,
  "text": "/upload@tele_photo_bot",
  "chat": {
    "id": -1002486692583,
    "is_forum": true,
    "title": "resources for d grind \ud83d\ude2c\ud83d\ude2c",
    "type": "supergroup"
  },
  "date": 1758043643,
  "message_id": 354,
  "from": {
    "first_name": "jolene",
    "id": 1797223820,
    "is_bot": false,
    "language_code": "en",
    "username": "jolneetan"
  }
}
```

We're only interested in `message.reply_to_message`. Let's inspect and see how it looks like:

```
{
  "channel_chat_created": false,
  "delete_chat_photo": false,
  "group_chat_created": false,
  "media_group_id": "14064031313798717",
  "photo": [
    {
      "height": 90,
      "width": 40,
      "file_id": "AgACAgUAAyEFAASUN-rnAAIBCmjJAta4ZmeW9eV5BJYKGf9Yy55oAAKWyzEbDeJIVsa_b2rRUlvLAQADAgADcwADNgQ",
      "file_size": 1189,
      "file_unique_id": "AQADlssxGw3iSFZ4"
    },
    {
      "height": 320,
      "width": 144,
      "file_id": "AgACAgUAAyEFAASUN-rnAAIBCmjJAta4ZmeW9eV5BJYKGf9Yy55oAAKWyzEbDeJIVsa_b2rRUlvLAQADAgADbQADNgQ",
      "file_size": 14417,
      "file_unique_id": "AQADlssxGw3iSFZy"
    },
    {
      "height": 800,
      "width": 360,
      "file_id": "AgACAgUAAyEFAASUN-rnAAIBCmjJAta4ZmeW9eV5BJYKGf9Yy55oAAKWyzEbDeJIVsa_b2rRUlvLAQADAgADeAADNgQ",
      "file_size": 58279,
      "file_unique_id": "AQADlssxGw3iSFZ9"
    },
    {
      "height": 1280,
      "width": 576,
      "file_id": "AgACAgUAAyEFAASUN-rnAAIBCmjJAta4ZmeW9eV5BJYKGf9Yy55oAAKWyzEbDeJIVsa_b2rRUlvLAQADAgADeQADNgQ",
      "file_size": 109993,
      "file_unique_id": "AQADlssxGw3iSFZ-"
    }
  ],
  "supergroup_chat_created": false,
  "chat": {
    "id": -1002486692583,
    "is_forum": true,
    "title": "resources for d grind \ud83d\ude2c\ud83d\ude2c",
    "type": "supergroup"
  },
  "date": 1758003914,
  "message_id": 266,
  "from": {
    "first_name": "jolene",
    "id": 1797223820,
    "is_bot": false,
    "language_code": "en",
    "username": "jolneetan"
  }
}
```

There are different photos for one photo, with the different resolutions. So I make sure to only download the highest resolution (ie. the last one in the array).

Main caveat: the replied message only refers to one message (the latest one) in the album. Meaning we only have access to the most recent photo in the album.

### So how do we access all photos in the album?

- Photos in the same album share the same `media_group_id`. We use this to groups items in the same `media_group_id` as one album.

#### Constraints

- Telegram doesn't provide an API to fetch messages by `media_group_id`. So we need to have a handler to listen for messages (particularly photos), and group them by `media_group_id`.

#### Current approach (not the best, but works for now)

    - Have a handler to listen for messages (particularly photos), and place the message in its corresponding bucket.
    - We can use an in-memory hash map for this: { media_group_id: Message[] }
    - CONS: potentially memory intensive. Also if the server goes down and the map is lost, unintuitive behaviour results. User would have to upload images one-by-one; can have a message to caveat this.
    - PROS: it works. And users can repeatedly upload an album (eg. to different gdrive folders), so long as the server is up.

### Working with Google Drive

The bot has to upload media into Google Drive. There are 2 main ways to do this:

1. Create a Service Account and use it to access Google Drive.
   - PROBLEM: This only works with Shared Drives (which are paid for, unlike the usual Personal Drives)
2. Allow the app (ie. this bot) to use my Google account to upload images into a Folder.
   - PROBLEM: The folder has to be shared with my gmail, for the bot to work.
   - PROBLEM: When the bot first starts, it runs the Google OAuth flow -> opens browser window for me to login -> token generated, used to authenticate future sessions. This is all well and good until the token expires / becomes invalid. In which case, either a) `refresh_token` inside `oauth_token.json` is used automatically to generate a new token, or b) I'd have to run the OAuth flow outside of Docker (which I'm running the server in), then pass in the new token file.

I went with approach 2 since I wanted this bot to work with Personal Drives.

## Expected behaviors:

1. When server just starts, trying to upload an album will only upload the latest photo.
2. A file created on the server should be deleted after successful / unsuccessful uploading (so client can retry without overloading our server)

3. WIP: Support video uploads. Currently, only photos in an album are uploaded.
4. WIP: Support recursive folder names

## 5) Future Extensions:

### 5.1) Caching

To upload an album, I need to get every message with the same `media_group_id`. But because Telegram doesn't provide an API to get message by `media_group_id` (maybe bcause they don't store messages after a certain period of time..? Not sure), for every album that comes in I'll need to store the messages by `media_group_id` in memory.

**PROBLEMS:**

- Potentially memory-intensive, especially with extended use.

**POTENTIAL SOLUTION:**

- We can use a cache (eg. Redis, or implement a simple cache of our own). For each chat, cache eg. the 20 most recent `media_group_id` and their messages. Once expired, evict the `media_group_id` from cache. We go by FIFO because the behaviour is easiest to explain to users.
- We can also store in cache the chats whose media group IDs we are currently tracking (mapped to their `media_group_id`s, eg. `{chat_id: [media_group_id_1, media_group_id_2...]}`). Give each entry a TTL. Once expired, remove the `chat_id` from cache and all its associated `media_group_id`s we are currently tracking.
- This prevents overloading our server, and the behaviour makes sense in user's perspectives as well.

---

async def upload_handler(update: Update, context: ContextTypes.DEFAULT_TYPE): # check if message is a reply to a photo
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
    except Exception as e:
        print("[upload()] Failed to upload images: ", e)
        await update.message.reply_text("An error occurred. Please try again.")

    finally:
        print("[upload_handler()] Deleting files...")
        for file in created_files:
            delete_file(file)
        print("[upload_handler()] Successfully deleted files")
