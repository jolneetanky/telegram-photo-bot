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
