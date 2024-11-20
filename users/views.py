# users/views.py
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import UserSerializer
from django.contrib.auth.hashers import check_password
from .models import User
from rest_framework.views import APIView
from .models import HistoryTitle
from .models import Chat
from .serializers import ChatSerializer
from django.contrib.auth.hashers import check_password
from .serializers import PasswordChangeSerializer


@api_view(['POST'])
def signup(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            # Save the new user to the database
            user = serializer.save()
            return Response({
                'message': 'User created successfully',
                'user_id': user.user_id,
                'user_name': user.user_name,
                'email': user.email
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    def post(self, request):
        # Extract credentials
        email = request.data.get('email')
        password = request.data.get('password')
        
        if not email or not password:
            return Response({"error": "Email and password are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Get user by email
            user = User.objects.get(email=email)
            
            # Verify password
            if check_password(password, user.user_password):  # If passwords match
                return Response({
                    "message": "Login successful",
                    "user": {
                        "id": user.user_id,
                        "name": user.user_name,
                        "email": user.email
                    }
                }, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Invalid password."}, status=status.HTTP_401_UNAUTHORIZED)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        
class HistoryAPIView(APIView):
    def get(self, request, user_id):
        # Fetch history for the given user_id
        history = HistoryTitle.objects.filter(user_id=user_id).order_by('-time_stamp')
        
        if not history.exists():
            return Response({"message": "No history found for this user."}, status=status.HTTP_404_NOT_FOUND)

        # Serialize the data
        data = [
            {
                "chat_id": record.chat_id,
                "chat_name": record.chat_name,
                "time_stamp": record.time_stamp,
                "user_id": record.user_id
            }
            for record in history
        ]
        
        return Response(data, status=status.HTTP_200_OK)
    
class ChatHistoryAPIView(APIView):
    def get(self, request, chat_id):
        # Fetch messages from the Chat table for the given Chat_ID
        chat_messages = Chat.objects.filter(chat_id=chat_id).order_by('time_stamp')
        
        if not chat_messages.exists():
            return Response({"message": "No messages found for this chat."}, status=status.HTTP_404_NOT_FOUND)
        
        # Serialize the chat messages
        serializer = ChatSerializer(chat_messages, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class UserDetailAPIView(APIView):
    def get(self, request, user_id):
        try:
            # Fetch user based on user_id
            user = User.objects.get(user_id=user_id)
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"message": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        


class ChangePasswordAPIView(APIView):
    def post(self, request):
        # Deserialize the incoming request data
        serializer = PasswordChangeSerializer(data=request.data)
        
        if serializer.is_valid():
            email = serializer.validated_data['email']
            old_password = serializer.validated_data['old_password']
            new_password = serializer.validated_data['new_password']

            try:
                # Fetch the user based on the provided email
                user = User.objects.get(email=email)
                
                # Check if the old password matches
                if not user.check_password(old_password):
                    return Response({"message": "Old password is incorrect."}, status=status.HTTP_400_BAD_REQUEST)
                
                # Set and save the new password
                user.set_password(new_password)
                user.save()

                return Response({"message": "Password updated successfully."}, status=status.HTTP_200_OK)
            
            except User.DoesNotExist:
                return Response({"message": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)