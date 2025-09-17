# ml/predict_local.py
import tensorflow as tf
from PIL import Image
import numpy as np
import sys
from pathlib import Path

# Get image path from command line
if len(sys.argv) < 2:
    print("Usage: python ml/predict_local.py <image_path>")
    sys.exit(1)

img_path = Path(sys.argv[1])

# Load and preprocess image
img = Image.open(img_path).convert('RGB').resize((224, 224))
arr = np.array(img) / 255.0
inp = np.expand_dims(arr, 0)

# Load trained model (Keras SavedModel folder)
model = tf.keras.models.load_model("ml/models/disease_classifier.keras")


# Predict
pred = model.predict(inp)[0]
cls = int(pred.argmax())
confidence = float(pred[cls])

print("✅ Predicted class index:", cls, "| confidence:", confidence)
