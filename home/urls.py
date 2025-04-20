from django.urls import path
from . import views

#URLConfig
urlpatterns = [ 
    path('registration/',views.open_registration,name='registration'),
    path('login/',views.open_login,name='login'),
    path('landing/', views.open_home, name='landing'),
    path('verify-email/<str:uidb64>/<str:token>/', views.verify_email, name='verify_email')
]