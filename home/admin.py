from django.contrib import admin
from .models import CustomUser, Candidate, Election, Vote
from .notifications import notify_users_about_election
from django.contrib.auth.admin import UserAdmin

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'voter_id', 'kyc_verified', 'is_active', 'is_staff')
    list_filter = ('kyc_verified', 'is_staff', 'is_superuser')

    fieldsets = UserAdmin.fieldsets + (
        ('KYC Details', {
            'fields': ('date_of_birth', 'address','citizenship_id','mothers_name','fathers_name', 'kyc_verified',),
        }),
    )

    list_editable = ('kyc_verified',)  # Allow inline approval from the user list view

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
