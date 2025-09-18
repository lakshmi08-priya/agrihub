from fastapi import FastAPI, File, UploadFile

app = FastAPI(title="AgroLens API", version="0.1.0")


@app.post("/predict/disease")
async def predict_disease(file: UploadFile = File(...)):
    return {
        "disease": "Leaf Blight",
        "confidence": 0.87,
        "filename": file.filename
    }


@app.post("/predict/pest")
async def predict_pest(file: UploadFile = File(...)):
    return {
        "pest": "Aphid",
        "confidence": 0.92,
        "filename": file.filename,
        "bbox": [100, 120, 250, 300]
    }


@app.post("/predict/soil")
async def predict_soil(file: UploadFile = File(...)):
    return {
        "soil_type": "Black Soil",
        "confidence": 0.89,
        "filename": file.filename
    }


@app.post("/predict/chat")
async def predict_chat(query: str):
    return {
        "query": query,
        "response": "This is a helpful farming suggestion."
    }
 