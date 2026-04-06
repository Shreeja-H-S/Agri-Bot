import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras import layers, models
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import EarlyStopping

DATASET_DIR = "reduced_dataset"
IMG_SIZE = (128, 128)
BATCH_SIZE = 32
NUM_CLASSES = 13
MODEL_SAVE_PATH = "backend/disease/agri_model.h5"

# Data generators
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=20,
    zoom_range=0.2,
    horizontal_flip=True,
    validation_split=0.2
)

train_gen = train_datagen.flow_from_directory(
    DATASET_DIR,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    subset='training'
)

val_gen = train_datagen.flow_from_directory(
    DATASET_DIR,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    subset='validation'
)

print("Class indices:", train_gen.class_indices)

# Build model
base_model = MobileNetV2(input_shape=(128, 128, 3), include_top=False, weights='imagenet')
base_model.trainable = False

model = models.Sequential([
    base_model,
    layers.GlobalAveragePooling2D(),
    layers.Dense(128, activation='relu'),
    layers.Dense(NUM_CLASSES, activation='softmax')
])

early_stop = EarlyStopping(monitor='val_loss', patience=2, restore_best_weights=True)

# Phase 1 — train top layers only
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
print("\n--- Phase 1: Training top layers ---")
model.fit(train_gen, validation_data=val_gen, epochs=5, callbacks=[early_stop])

# Phase 2 — fine-tune last 20 layers of base model
base_model.trainable = True
for layer in base_model.layers[:-20]:
    layer.trainable = False

model.compile(optimizer=tf.keras.optimizers.Adam(1e-5),
              loss='categorical_crossentropy', metrics=['accuracy'])
print("\n--- Phase 2: Fine-tuning last 20 layers ---")
model.fit(train_gen, validation_data=val_gen, epochs=5, callbacks=[early_stop])

# Save model
model.save(MODEL_SAVE_PATH)
print(f"\nModel saved to {MODEL_SAVE_PATH}")
