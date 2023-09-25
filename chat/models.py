from django.db import models
from api.models import Users


# Create your models here.
class ChatBaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
     
    class Meta:
        abstract = True


class MessageRecord(ChatBaseModel):
    CONTENT_TYPE = (
        ("text" , "Text"),
        ("image", "Image"),
        ("docs", "Docs"),
        ("video", "Video"),
        ("audio", "Audio"),
    )

    sender = models.ForeignKey(Users, on_delete=models.CASCADE, related_name="message_sender")
    receiver = models.ForeignKey(Users, on_delete=models.CASCADE, related_name="message_receiver")
    message = models.TextField(null=False, blank=False)
    message_type = models.CharField(max_length=10, choices=CONTENT_TYPE, default="text")
    is_read = models.BooleanField(default=False)
    parent_message = models.ForeignKey(
        "self", on_delete=models.CASCADE, limit_choices_to={'parent_message': None}, null=True, blank=True
    )
    is_delivered = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f'Sent By: {self.sender.username} - Received By : {self.receiver.username}'
    
    class Meta:
        indexes = [
            models.Index(fields=['sender']),
            models.Index(fields=['receiver']),
            models.Index(fields=['created_at'])
        ]
