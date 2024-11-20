from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from .models import User
from .models import Chat

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  # password will be write-only

    class Meta:
        model = User
        fields = ['user_name', 'email', 'password']  # Add any additional fields as necessary

    def create(self, validated_data):
        # Hash the password before saving
        password = validated_data.pop('password')  # Get the password from validated data
        validated_data['user_password'] = make_password(password)  # Hash the password
        user = User.objects.create(**validated_data)  # Create the user with the validated data
        return user
    
class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ['chat_message_id', 'chat_text', 'chat_id', 'sender_type', 'time_stamp']

class PasswordChangeSerializer(serializers.Serializer):
    email = serializers.EmailField()
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)