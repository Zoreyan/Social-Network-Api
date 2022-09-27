from rest_framework import serializers
from .models import *


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='name', read_only=True)
    class Meta:
        model = Comment
        fields = ['id', 'user', 'post', 'text']


class LikeSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='name', read_only=True)
    post = serializers.SlugRelatedField(slug_field='title', read_only=True)
    class Meta:
        model = Like
        fields = '__all__'



class PostSerializer(serializers.ModelSerializer):
    comment = CommentSerializer(many=True)
    like = LikeSerializer(many=True)
    user = serializers.SlugRelatedField(slug_field='name', read_only=True)
    class Meta:
        model = Post
        exclude = ['topic',]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
    
    def create(self, validated_data):
        user = super().create(validated_data)
        password = validated_data['password']
        user.set_password(password)
        user.save()
        return 