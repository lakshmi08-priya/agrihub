# ml/train_classification.py
import tensorflow as tf
from tensorflow.keras import layers, models
import os

# Paths and configs
DATA_DIR = 'ml/data/processed'
BATCH = 32
IMG_SIZE = (224, 224)
EPOCHS = 6

# Load training and validation datasets
train_ds = tf.keras.preprocessing.image_dataset_from_directory(
    os.path.join(DATA_DIR, 'train'),
    image_size=IMG_SIZE,
    batch_size=BATCH
)

val_ds = tf.keras.preprocessing.image_dataset_from_directory(
    os.path.join(DATA_DIR, 'val'),
    image_size=IMG_SIZE,
    batch_size=BATCH
)

# Number of classes
num_classes = len(train_ds.class_names)

# Build model using MobileNetV2 backbone
base = tf.keras.applications.MobileNetV2(
    input_shape=IMG_SIZE + (3,),
    include_top=False,
    weights='imagenet'
)
base.trainable = False

inputs = tf.keras.Input(shape=IMG_SIZE + (3,))
x = tf.keras.applications.mobilenet_v2.preprocess_input(inputs)
x = base(x, training=False)
x = layers.GlobalAveragePooling2D()(x)
x = layers.Dropout(0.2)(x)
outputs = layers.Dense(num_classes, activation='softmax')(x)

model = models.Model(inputs, outputs)

# Compile model
model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

# Train model
model.fit(train_ds, validation_data=val_ds, epochs=EPOCHS)

# ✅ Save model in Keras 3 format
model.save("ml/models/disease_classifier.keras")
print("✅ Saved model to ml/models/disease_classifier.keras")

# Load test dataset
test_ds = tf.keras.utils.image_dataset_from_directory(
    os.path.join(DATA_DIR, "test"),
    image_size=IMG_SIZE,
    batch_size=BATCH,
    shuffle=False
)

# Evaluate on test dataset
loss, acc = model.evaluate(test_ds)
print(f"✅ Test Accuracy: {acc:.4f}")
