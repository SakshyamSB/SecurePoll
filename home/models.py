from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    voter_id = models.CharField(max_length=20, unique=True)  # Ensure voter_id is unique

    def __str__(self):
        return self.username
    
class Candidate(models.Model):
    full_name = models.CharField(max_length=100)
    party_name = models.CharField(max_length=100)
    profile_picture = models.ImageField(upload_to='candidate_profiles/', null=True, blank=True)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.full_name}"