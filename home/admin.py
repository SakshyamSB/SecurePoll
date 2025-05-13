from django.contrib import admin
from .models import CustomUser , Candidate ,Election, Vote
# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Candidate)
admin.site.register(Election)
admin.site.register(Vote)