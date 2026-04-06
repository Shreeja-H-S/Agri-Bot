from rest_framework import serializers
from .models import DiseasePrediction


class DiseasePredictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiseasePrediction
        fields = ['id', 'user', 'image', 'result', 'confidence', 'created_at']
        read_only_fields = ['user', 'result', 'confidence', 'created_at']
