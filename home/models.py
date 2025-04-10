from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    voter_id = models.CharField(max_length=20, unique=True)  # Ensure voter_id is unique

    def __str__(self):
        return self.username
    
