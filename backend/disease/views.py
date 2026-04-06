from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from PIL import Image
import numpy as np
from .models import DiseasePrediction
from .serializers import DiseasePredictionSerializer
from .ml_model import load_model


def predict_image(image_file):
    img = Image.open(image_file).convert("RGB")
    img = img.resize((128, 128))
    img_array = np.array(img, dtype=np.float32)
    img_array = img_array / 255.0
    img_array = np.expand_dims(img_array, axis=0)  # shape: (1, 128, 128, 3)

    print("Image shape:", img_array.shape)
    print("Image min:", img_array.min(), "max:", img_array.max())

    model = load_model()
    prediction = model.predict(img_array, verbose=0)
    print("Prediction array:", prediction)

    # Class mapping from training class_indices
    class_names = [
        'Apple___Apple_scab',
        'Apple___Black_rot',
        'Apple___Cedar_apple_rust',
        'Apple___healthy',
        'Grape___Black_rot',
        'Grape___Esca_(Black_Measles)',
        'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)',
        'Grape___healthy',
        'Orange___Haunglongbing_(Citrus_greening)',
        'Potato___Early_blight',
        'Potato___Late_blight',
        'Potato___healthy',
        'Tomato___Bacterial_spot',
    ]

    predicted_index = int(np.argmax(prediction[0]))
    confidence = float(np.max(prediction[0]))
    label = class_names[predicted_index] if predicted_index < len(class_names) else f"Class {predicted_index}"
    print(f"Predicted: {label} ({confidence * 100:.2f}%)")
    return label, round(confidence, 4)


class DiseasePredictView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        serializer = DiseasePredictionSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user if request.user.is_authenticated else None
            image = request.FILES.get('image')
            if not image:
                return Response({"status": "error", "message": "No image uploaded."}, status=status.HTTP_400_BAD_REQUEST)
            try:
                result, confidence = predict_image(image)
                predicted_class = result
            except Exception as e:
                import traceback
                traceback.print_exc()
                print("ERROR:", str(e))
                return Response({"status": "error", "message": str(e)})

            record = serializer.save(user=user, result=predicted_class, confidence=confidence)
            return Response(
                {"status": "success", "data": DiseasePredictionSerializer(record).data},
                status=status.HTTP_201_CREATED
            )
        return Response({"status": "error", "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
