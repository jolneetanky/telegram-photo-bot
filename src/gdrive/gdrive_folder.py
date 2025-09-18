from typing import Optional
import re

class GDriveFolder:
    """
    Extracts and returns the folder ID from a Google Drive folder link.
    Returns None if invalid.
    """
    @staticmethod
    def _extract_folder_id(folder_link: str) -> Optional[str]:
        pattern = r"https?://drive\.google\.com/drive/folders/([a-zA-Z0-9_-]+)"
        match = re.match(pattern, folder_link)
        if match:
            return match.group(1)
        return None

    """Checks if the link looks like a valid Google Drive folder link."""
    @staticmethod
    def is_valid_drive_folder_link(folder_link: str) -> bool:
        return GDriveFolder._extract_folder_id(folder_link) is not None
    
    def __init__(self, link: str):
        self.link = link
        self.id = GDriveFolder._extract_folder_id(link)