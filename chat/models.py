from main.models import User
from django.db import models


class Friend(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='friend')
    
    def __str__(self):
        return self.user.name

class ChatMessage(models.Model):
    body = models.TextField(null=True)
    file = models.FileField(upload_to='messages/', null=True)
    msg_sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="msg_sender")
    msg_receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="msg_receiver")
    seen = models.BooleanField(default=False)
    
    def __str__(self):
        return self.body

