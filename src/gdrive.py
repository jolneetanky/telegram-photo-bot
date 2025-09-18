import os
from dotenv import load_dotenv
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# for get_drive_service()
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

load_dotenv()

"""
Builds drive service with oath credentials (so we can access user functions!)
"""
def get_drive_service(SCOPES: list[str]):
    TOKEN_PATH = os.getenv("GOOGLE_OAUTH_TOKEN_FILE")
    CREDENTIALS_PATH = os.getenv("GOOGLE_OAUTH_CREDENTIALS_FILE")
    """Authenticate and return a Drive API service for the user."""
    creds = None
    # NOTE: this is wrt project root.
    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
    # refresh credits if needed
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # trigger auth flow
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_PATH, SCOPES)
            creds = flow.run_local_server(port=0)
        # save token for reuse
        with open(TOKEN_PATH, 'w') as token:
            token.write(creds.to_json())

    return build('drive', 'v3', credentials=creds)

class GDriveService:
    def __init__(self, scopes: list[str], google_service_account_file: str):
        self.scopes = scopes
        self.google_service_account_file = google_service_account_file

        self.drive_service = get_drive_service(scopes)

    """
    Returns ID of an existing folder, or None if it doesn't exist
    """
    def _get_folder(self, folder_name: str, parent_folder_id) -> list: 
        query = f"'{parent_folder_id}' in parents and trashed=false"

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
                return folder['id']

        return None

    """
    Given a list of `folder_names` and a `root_folder_id`, creates the folder_names respecting the hierarchy (left -> right), within `root_folder_id`.
    If no `root_folder_id` is given, it will just create a new folder rooted at the first folder in `folder_names`.

    TEST CASES:
    1. `root_folder_id` passed in -> should create the nested folder_names in root_folder_id.
    2. `root_folder_id` not passed in -> should create the folders as they are, ultimately creating a new root folder.
    3. if `folder_names` is empty, nothing happens.
    """
    def create_folders_if_not_exists(self, root_folder_id, folder_names: list[str] = []) -> str:
        if not folder_names:
            print("[get_leaf_folder_id()] No paths to create folders for.")
            return

        parent_id = root_folder_id

        for folder_name in folder_names:
            if parent_id == "":
                parent_id = self._create_folder(folder_name, parent_id)
                continue

            # create folder if it doesn't exist.
            folder_id = self._get_folder(folder_name, parent_id)
            if folder_id:
                parent_id = folder_id
                continue

            parent_id = self._create_folder(folder_name, parent_id)

        return parent_id

            # if the current 
        
        # return self._helper(0, paths)

    # returns folder ID
    def _create_folder(self, folder_name: str, parent_folder_id: str = None) -> str:
        print("create_folder_if_not_exists()")

        # try:
        #     folder_id = self._get_folder(folder_name, parent_folder_id)
        #     if folder_id:
        #         print("Folder already exists")
        #         return folder_id
        # except Exception as e:
        #     print("Failed to check if folder exists: ", e)
        #     raise e

        # if folder doesn't exist, create one
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