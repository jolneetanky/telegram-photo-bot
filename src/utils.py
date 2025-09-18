from telegram import Message, Update
from custom_types import MediaFile
import json
import os
import re
from typing import Optional

"""
Deletes a file from server.
"""
def delete_file(file: MediaFile) -> None:
    try:
        if os.path.exists(file.server_download_path):
            os.remove(file.server_download_path)
    except Exception as e:
        print(f"[delete_file()] Failed to delete {file.server_download_path}: {e}")


def pretty_print(obj):
    obj = obj.to_dict()
    print(json.dumps(obj, indent=2)) 

"""
Extracts and returns the folder ID from a Google Drive folder link.
Returns None if invalid.
"""
def extract_folder_id(folder_link: str) -> Optional[str]:
    pattern = r"https?://drive\.google\.com/drive/folders/([a-zA-Z0-9_-]+)"
    match = re.match(pattern, folder_link)
    if match:
        return match.group(1)
    return None

"""Checks if the link looks like a valid Google Drive folder link."""
def is_valid_drive_folder_link(folder_link: str) -> bool:
    return extract_folder_id(folder_link) is not None