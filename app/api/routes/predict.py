from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
from app.core import config
from pathlib import Path
import shutil

router = APIRouter()

# Dummy prediction function
def dummy_predict(file_path: Path):
    # In real scenario: load your ML model and return prediction
    return {"prediction": "healthy", "confidence": 0.95}

# ----------------------------
# Endpoint for prediction
# ----------------------------
@router.post("/")
async def predict(file: UploadFile = File(...)):
    # Save uploaded file to RAW_BUCKET
    file_path = config.RAW_BUCKET / file.filename
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Call dummy prediction
    result = dummy_predict(file_path)

    # Optionally, move processed files to PROCESSED_BUCKET
    processed_path = config.PROCESSED_BUCKET / file.filename
    shutil.copy(file_path, processed_path)

    return JSONResponse(content=result)
