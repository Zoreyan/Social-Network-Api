from .models import ChatMessage
from rest_framework import serializers



class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = '__all__'