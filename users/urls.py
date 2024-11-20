from django.urls import path
from . import views
from .views import LoginAPIView
from .views import HistoryAPIView
from .views import ChatHistoryAPIView
from .views import UserDetailAPIView
from .views import ChangePasswordAPIView

urlpatterns = [
   path('signup/', views.signup, name='signup'),
   path('login/', LoginAPIView.as_view(), name='login'),
   path('history/<int:user_id>/', HistoryAPIView.as_view(), name='history'),
   path('chat/history/<int:chat_id>/', ChatHistoryAPIView.as_view(), name='chat-history'),
   path('user/details/<int:user_id>/', UserDetailAPIView.as_view(), name='user-details'),
   path('user/change-password/', ChangePasswordAPIView.as_view(), name='change-password'),
   
]