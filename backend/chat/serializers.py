from rest_framework import serializers
from .models import Chat


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ['id', 'user', 'message', 'response', 'created_at']
        read_only_fields = ['user', 'response', 'created_at']
