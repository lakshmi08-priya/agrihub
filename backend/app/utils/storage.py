import os
import tempfile
from fastapi import UploadFile

TEMP_UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "tmp_uploads")
os.makedirs(TEMP_UPLOAD_DIR, exist_ok=True)

async def save_upload_temp(file: UploadFile) -> str:
    """
    Save an UploadFile to a temp location and return the path.
    ML code can read from this path.
    """
    suffix = os.path.splitext(file.filename)[1]
    tmp_name = f"{file.filename or 'upload'}-{os.urandom(6).hex()}{suffix}"
    tmp_path = os.path.join(TEMP_UPLOAD_DIR, tmp_name)
    contents = await file.read()
    with open(tmp_path, "wb") as f:
        f.write(contents)
    return tmp_path
