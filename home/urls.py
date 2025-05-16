from django.urls import path
from . import views

#URLConfig
urlpatterns = [ 
    path('registration/',views.open_registration,name='registration'),
    path('login/',views.open_login,name='login'),
    path('landing/', views.open_home, name='landing'),
    path('verify-email/<str:uidb64>/<str:token>/', views.verify_email, name='verify_email'),
    path('cast-vote/', views.cast_vote, name='cast_vote'),
    path('submit-vote/<int:election_id>/', views.submit_vote, name='submit_vote'),
    path('results/', views.election_results, name='election_results'),
    path('election-results/', views.election_results, name='election_results'),
    path('my-info/', views.my_info, name='my_info'),
    path('logout/', views.user_logout, name='logout'),


    path('verify-email/<str:uidb64>/<str:token>/', views.verify_email, name='verify_email'),
    path('cast-vote/', views.cast_vote, name='cast_vote'),
    path('submit-vote/<int:election_id>/', views.submit_vote, name='submit_vote'),
    path('results/', views.election_results, name='election_results'),
    path('election-results/', views.election_results, name='election_results'),
    path('my-info/', views.my_info, name='my_info'),


]