from django.urls import path
from .views import course_chat_room

app_name  = 'chat'

urlpatterns = [
    path('room/<int:book_id>',course_chat_room,name='course_chat_room')
]