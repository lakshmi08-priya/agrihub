from fastapi import APIRouter, UploadFile, File, Form
from typing import Dict, Any
import uuid
from ..utils.storage import save_upload_temp

router = APIRouter()

# --- helper: mock response templates ---
def mock_disease(filename: str) -> Dict[str, Any]:
    return {"disease": "Leaf Blight", "confidence": 0.87, "filename": filename}

def mock_pest(filename: str) -> Dict[str, Any]:
    return {"pest": "Aphid", "confidence": 0.92, "filename": filename, "bbox": [100, 120, 250, 300]}

def mock_soil(filename: str) -> Dict[str, Any]:
    return {"soil_type": "Loamy", "confidence": 0.81, "filename": filename}

# --- endpoints ---
@router.post("/disease", summary="Predict plant disease from image (multipart/form-data)")
async def predict_disease(file: UploadFile = File(...)):
    """
    Accepts an uploaded image file and returns a disease prediction.
    For now this is a mock response. Replace call to ML function when available.
    """
    # Save temporary file locally for the ML model to read (if needed)
    path = await save_upload_temp(file)
    # TODO: call your ML function, e.g. result = predict_disease_model(path)
    result = mock_disease(file.filename)
    return result

@router.post("/pest", summary="Detect pests from image")
async def predict_pest(file: UploadFile = File(...)):
    path = await save_upload_temp(file)
    # TODO: call ML model
    result = mock_pest(file.filename)
    return result

@router.post("/soil", summary="Classify soil from image")
async def classify_soil(file: UploadFile = File(...)):
    path = await save_upload_temp(file)
    # TODO: call ML model
    result = mock_soil(file.filename)
    return result

@router.post("/chat", summary="Chat / FAQ — text query")
async def chat(query: str = Form(...)):
    # TODO: connect to NLP prototype (DistilBERT / SentenceTransformers)
    answer = f"Mock answer to: {query}"
    return {"answer": answer}
