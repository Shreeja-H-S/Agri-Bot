import os
import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras import layers, models

MODEL_PATH = os.path.join(os.path.dirname(__file__), "agri_model.h5")

_model = None


def load_model():
    global _model
    if _model is None:
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(f"Model file not found at {MODEL_PATH}")
        _model = tf.keras.models.load_model(MODEL_PATH, compile=False)
        print("Model loaded from", MODEL_PATH)
    return _model
