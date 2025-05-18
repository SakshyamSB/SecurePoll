from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from .notifications import notify_users_about_election

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
    
class Election(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    candidates = models.ManyToManyField('Candidate', related_name='election')

    def __str__(self):
        return self.name

    def is_active(self):
        from django.utils import timezone
        now = timezone.now()
        return self.start_date <= now <= self.end_date
    
class Vote(models.Model):
    voter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    candidate = models.ForeignKey('Candidate', on_delete=models.CASCADE)
    election = models.ForeignKey('Election', on_delete=models.CASCADE)
    voted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('voter', 'election')  # Prevent multiple votes in same election

    def __str__(self):
        return f"{self.voter} voted for {self.candidate} in {self.election}"

