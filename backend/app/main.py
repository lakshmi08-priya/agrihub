from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from tensorflow.keras.models import load_model
from PIL import Image
import numpy as np
import io

app = FastAPI(title="AgroLens Backend")

# Load your Keras model once when the server starts
model = load_model("../../ml/models/disease_classifier.keras")

@app.get("/")
async def root():
    return {"status": "ok", "message": "AgroLens backend is running 🚀"}

@app.post("/predict_file")
async def predict_file(file: UploadFile = File(...)):
    # Read the image
    contents = await file.read()
    image = Image.open(io.BytesIO(contents)).convert("RGB")

    # Preprocess (resize to model input, e.g. 224x224)
    img_array = image.resize((224, 224))   # adjust if your model expects different size
    img_array = np.array(img_array) / 255.0
    img_array = np.expand_dims(img_array, axis=0)  # shape: (1, 224, 224, 3)

    # Run prediction
    prediction = model.predict(img_array)
    predicted_class = int(np.argmax(prediction[0]))
    confidence = float(np.max(prediction[0]))

    return JSONResponse({
        "predicted_class": predicted_class,
        "confidence": confidence
    })
