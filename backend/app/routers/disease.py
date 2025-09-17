from fastapi import APIRouter, UploadFile, File, HTTPException
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import io
from PIL import Image

router = APIRouter()

# Load model once at startup
MODEL_PATH = "ml/models/disease_classification.keras"
try:
    model = load_model(MODEL_PATH)
except Exception as e:
    raise RuntimeError(f"Error loading model: {e}")

# Example class names (replace with your dataset classes)
CLASS_NAMES = ["Healthy", "Bacterial Blight", "Leaf Spot", "Rust"]

@router.post("/predict_disease/")
async def predict_disease(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        img = Image.open(io.BytesIO(contents)).convert("RGB")
        img = img.resize((224, 224))  # adjust if your model uses different input size
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0) / 255.0

        predictions = model.predict(img_array)
        predicted_class = CLASS_NAMES[np.argmax(predictions)]
        confidence = float(np.max(predictions))

        return {
            "predicted_class": predicted_class,
            "confidence": round(confidence, 4)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {e}")
