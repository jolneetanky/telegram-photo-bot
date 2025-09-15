import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# from dotenv import load_dotenv

# load_dotenv()

# oauth setup
# from __future__ import print_function
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

"""
Builds drive service with oath credentials (so we can access user functions!)
"""
def get_drive_service(SCOPES: list[str]):
    """Authenticate and return a Drive API service for the user."""
    creds = None
    # NOTE: this is wrt project root.
    if os.path.exists('../oauth_token.json'):
        creds = Credentials.from_authorized_user_file('../oauth_token.json', SCOPES)
    # refresh credits if needed
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # trigger auth flow
            flow = InstalledAppFlow.from_client_secrets_file(
                '../oauth_credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # save token for reuse
        with open('../oauth_token.json', 'w') as token:
            token.write(creds.to_json())

    return build('drive', 'v3', credentials=creds)

class GDriveService:
    def __init__(self, scopes: list[str], google_service_account_file: str):
        self.scopes = scopes
        self.google_service_account_file = google_service_account_file

        # credentials = service_account.Credentials.from_service_account_file(google_service_account_file, scopes=scopes)
        # self.credentials = credentials
        # self.drive_service = build('drive', 'v3', credentials=credentials)
        self.drive_service = get_drive_service(scopes)

    """
    Creates folder if it doens't exist, and returns its ID.
    """
    def _folder_exists(self, folder_name: str, parent_folder_id) -> bool: 
        query = f"'{parent_folder_id}' in parents"

        results = self.drive_service.files().list(
            q=query,
            fields="nextPageToken, files(id, name)",
            pageSize=1000,
            supportsAllDrives=True  # important if using shared drives
        ).execute()

        folders = results.get('files', [])

        for folder in folders:
            print(f"Folder: {folder['name']} (ID: {folder['id']})")
            if folder_name == folder['name']:
                return True

        return False

    def create_folder_if_not_exists(self, folder_name: str, parent_folder_id: str = None) -> str:
        print("create_folder_if_not_exists()")

        try:
            if self._folder_exists(folder_name, parent_folder_id):
                print("Folder already exists")
                return
        except Exception as e:
            print("Failed to check if folder exists: ", e)
            raise e

        # scan through folders - if they exist, then just return

        print("SERVICE ACCOUNT FILE", self.google_service_account_file)
        """Create a folder in Google Drive and return its ID."""
        folder_metadata = {
            'name': folder_name,
            "mimeType": "application/vnd.google-apps.folder",
            'parents': [parent_folder_id] if parent_folder_id else []
        }

        try:
            created_folder = self.drive_service.files().create(
                body=folder_metadata,
                fields='id'
            ).execute()

            print(f'Created Folder ID: {created_folder["id"]}')
            return created_folder["id"]
        except Exception as e:
            print("Failed to create folder", e)
            raise e

    def upload_file(self, file_path, file_name, mime_type='image/png', parent_folder_id=None):
        print("[GDriveService.upload_file()]")
        """Upload a file to Google Drive."""
        file_metadata = {
        'name': file_name,
        'parents': [parent_folder_id] if parent_folder_id else []
        }
        # media = MediaFileUpload(file_path, mimetype=mime_type, resumable=True)
        media = MediaFileUpload(file_path, mimetype=mime_type, resumable=True)
        try:
            file = self.drive_service.files().create(
            body=file_metadata, media_body=media, fields='id').execute()
            print(f"Uploaded file with ID: {file.get('id')}")
        except Exception as e:
            print("Failed up to upload file: ", e)
            raise e


# Define the Google Drive API scopes and service account file path
# SCOPES = ['https://www.googleapis.com/auth/drive']
# GDRIVE_ROOT_FOLDER_ID = os.getenv("GDRIVE_ROOT_FOLDER_ID")
# SERVICE_ACCOUNT_FILE = os.getenv("SERVICE_ACCOUNT_FILE")

# credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# drive_service = build('drive', 'v3', credentials=credentials)

# def create_folder_if_not_exists(folder_name: str, parent_folder_id: str = None):
#     print("create_folder_if_not_exists()")


#     print("SERVICE ACCOUNT FILE", SERVICE_ACCOUNT_FILE)
#     """Create a folder in Google Drive and return its ID."""
#     folder_metadata = {
#         'name': folder_name,
#         "mimeType": "application/vnd.google-apps.folder",
#         'parents': [parent_folder_id] if parent_folder_id else []
#     }

#     created_folder = drive_service.files().create(
#         body=folder_metadata,
#         fields='id'
#     ).execute()

#     print(f'Created Folder ID: {created_folder["id"]}')
#     return created_folder["id"]

# def upload_file(file_path, file_name, mime_type='text/plain', parent_folder_id=None):
#     """Upload a file to Google Drive."""
#     file_metadata = {
#     'name': file_name,
#     'parents': [parent_folder_id] if parent_folder_id else []
#     }
#     media = MediaFileUpload(file_path, mimetype=mime_type, resumable=True)
#     file = drive_service.files().create(
#     body=file_metadata, media_body=media, fields='id').execute()
#     print(f"Uploaded file with ID: {file.get('id')}")