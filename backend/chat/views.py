from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import Chat
from .serializers import ChatSerializer


def get_bot_response(message):
    msg = message.lower()
    if any(w in msg for w in ['hello', 'hi', 'hey', 'greetings']):
        return "Hello! Welcome to AgriBot. How can I help you today?"
    elif any(w in msg for w in ['disease', 'infection', 'sick', 'infected', 'problem']):
        return "Please upload a plant image on the prediction page and I'll identify the disease for you."
    elif any(w in msg for w in ['leaf', 'leaves', 'yellow', 'brown', 'spots', 'wilting']):
        return "Leaf issues can indicate fungal, bacterial, or nutrient deficiency. Try uploading an image for an accurate diagnosis."
    elif any(w in msg for w in ['water', 'irrigation', 'watering']):
        return "Most plants need watering when the top inch of soil is dry. Overwatering is a common cause of root rot."
    elif any(w in msg for w in ['fertilizer', 'nutrient', 'soil', 'compost']):
        return "Healthy soil is key. Use balanced NPK fertilizer and add compost to improve soil structure."
    elif any(w in msg for w in ['pest', 'insect', 'bug', 'aphid', 'worm']):
        return "Pests can damage crops quickly. Consider neem oil or insecticidal soap as organic solutions."
    elif any(w in msg for w in ['weather', 'rain', 'temperature', 'climate']):
        return "Weather greatly affects plant health. Protect plants from frost and ensure proper drainage during heavy rain."
    elif any(w in msg for w in ['help', 'what can you do', 'features']):
        return "I can help with plant disease detection, crop care tips, pest control, and general agriculture queries!"
    elif any(w in msg for w in ['bye', 'goodbye', 'thanks', 'thank you']):
        return "Goodbye! Happy farming. Feel free to come back anytime."
    else:
        return "I'm AgriBot, your agriculture assistant. Ask me about plant diseases, pests, soil, or upload an image for disease detection."


class ChatView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        serializer = ChatSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user if request.user.is_authenticated else None
            bot_response = get_bot_response(serializer.validated_data['message'])
            chat = serializer.save(user=user, response=bot_response)
            return Response(
                {"status": "success", "data": ChatSerializer(chat).data},
                status=status.HTTP_201_CREATED
            )
        return Response({"status": "error", "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
