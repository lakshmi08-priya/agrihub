import os
from fastapi import UploadFile

TEMP_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "uploads")
os.makedirs(TEMP_DIR, exist_ok=True)

async def save_upload(file: UploadFile) -> str:
    path = os.path.join(TEMP_DIR, file.filename)
    contents = await file.read()
    with open(path, "wb") as f:
        f.write(contents)
    return path
