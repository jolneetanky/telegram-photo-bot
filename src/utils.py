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