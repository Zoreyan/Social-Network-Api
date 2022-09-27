from django.urls import path

from .views import *

urlpatterns = [
    path('', messages),
    path('message/<str:pk>/', message),
    path('message-create/', messageCreate),
    path('message-update/<int:pk>/', messageUpdate),
    path('message-delete/<int:pk>/', messageDelete)
]