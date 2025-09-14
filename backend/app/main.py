from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import numpy as np
from keras.models import load_model
from PIL import Image
import io
import json

app = FastAPI(title="AgroLens Backend")

# Load model (⚠️ this will still fail if you don’t have the keras file)
# model = load_model("ml/models/disease_classifier.keras")

# Load class names
with open("ml/models/class_names.json", "r") as f:
    CLASS_NAMES = json.load(f)

@app.post("/predict_file")
async def predict_file(file: UploadFile = File(...)):
    contents = await file.read()
    image = Image.open(io.BytesIO(contents)).resize((224, 224))  # adjust size to model
    img_array = np.array(image) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    # ⚠️ Without model, return dummy result
    # predictions = model.predict(img_array)
    # predicted_class_index = np.argmax(predictions[0])
    predicted_class_index = 0  # dummy for now
    confidence = 0.95

    predicted_class_name = CLASS_NAMES[predicted_class_index]

    return JSONResponse({
        "predicted_class": predicted_class_name,
        "confidence": float(confidence)
    })

