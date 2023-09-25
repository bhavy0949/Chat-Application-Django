from django.contrib.auth.models import AbstractUser
from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken

# Create your models here.
class Users(AbstractUser):
    contact_number = models.PositiveBigIntegerField(db_index= True, unique=True, blank= True, null= True)
    birth_date = models.DateField(blank=True, null=True)
    is_online = models.BooleanField(default=False)
    private_channel_name = models.CharField(max_length=35, null=True, blank=True)
    last_activity = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def get_tokens_for_user(self):
        refresh = RefreshToken.for_user(self)
        return f"{str(refresh.access_token)}"
    

    def __str__(self):
        return self.username    