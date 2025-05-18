from django.contrib import admin
from .models import CustomUser, Candidate, Election, Vote
from .notifications import notify_users_about_election

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'voter_id', 'email', 'is_staff','is_active')
    list_filter = ('is_active',)

@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'party_name', 'approved')
    list_filter = ('approved',)

@admin.register(Election)
class ElectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date')
    def save_model(self, request, obj, form, change):
        is_new = obj.pk is None
        super().save_model(request, obj, form, change)
        if is_new:
            notify_users_about_election(obj)

@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('voter', 'candidate', 'election', 'voted_at')
    list_filter = ('election', 'voted_at')
