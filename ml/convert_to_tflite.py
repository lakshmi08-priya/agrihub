# ml/convert_to_tflite.py
import tensorflow as tf

# Load the .keras model (not .h5)
model = tf.keras.models.load_model("ml/models/disease_classifier.keras")

# Convert to TFLite
converter = tf.lite.TFLiteConverter.from_keras_model(model)
converter.optimizations = [tf.lite.Optimize.DEFAULT]  # quantization for smaller size
tflite_model = converter.convert()

# Save to file
with open("ml/models/disease_classifier.tflite", "wb") as f:
    f.write(tflite_model)

print("✅ TFLite model saved to ml/models/disease_classifier.tflite")
