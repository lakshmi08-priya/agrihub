import os
import uuid
from fastapi import UploadFile

UPLOAD_DIR = "backend/uploads"

# Ensure upload folder exists
os.makedirs(UPLOAD_DIR, exist_ok=True)

async def save_upload_temp(file: UploadFile) -> str:
    """
    Save uploaded file temporarily in backend/uploads and return the file path.
    """
    ext = os.path.splitext(file.filename)[1]  # keep original extension
    unique_name = f"{uuid.uuid4().hex}{ext}"
    file_path = os.path.join(UPLOAD_DIR, unique_name)

    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)

    return file_path
