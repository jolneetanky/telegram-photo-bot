class MediaFile:
    def __init__(self, id: str, name: str, server_download_path: str):
        self.id = id
        self.name = name
        self.server_download_path = server_download_path

# class GDriveFolder:
#     """
#     Extracts and returns the folder ID from a Google Drive folder link.
#     Returns None if invalid.
#     """
#     def _extract_folder_id(self, folder_link: str) -> Optional[str]:
#         pattern = r"https?://drive\.google\.com/drive/folders/([a-zA-Z0-9_-]+)"
#         match = re.match(pattern, folder_link)
#         if match:
#             return match.group(1)
#         return None

#     """Checks if the link looks like a valid Google Drive folder link."""
#     def _is_valid_drive_folder_link(self, folder_link: str) -> bool:
#         return self._extract_folder_id(folder_link) is not None
    
#     def __init__(self, link: str):
#         if not self._is_valid_drive_folder_link(link):
#             raise InvalidGDriveLinkError
        
#         self.link = link
#         self.id = self._extract_folder_id(link)
