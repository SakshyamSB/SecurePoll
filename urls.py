from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [ 
    path('registration/', views.open_registration, name='registration'),
    path('login/', views.open_login, name='login'),
    path('landing/', views.open_home, name='landing'),
    path('verify-email/<str:uidb64>/<str:token>/', views.verify_email, name='verify_email'),
    path('cast-vote/', views.cast_vote, name='cast_vote'),
    path('submit-vote/<int:election_id>/', views.submit_vote, name='submit_vote'),
    path('results/', views.election_results, name='election_results'),
    path('election-results/', views.election_results, name='election_results'),
    path('my-info/', views.my_info, name='my_info'),
    path('logout/', views.user_logout, name='logout'),

    path('password-reset/', auth_views.PasswordResetView.as_view(
    template_name='home/forms/password_reset_form.html',  
    email_template_name='home/email/password_reset_email.html',
    success_url='/password-reset/done/',
    ), name='password_reset'),

    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='home/email/password_reset_done.html'
    ), name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='home/email/password_reset_confirm.html',
        success_url='/reset/done/',
    ), name='password_reset_confirm'),

    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='home/email/password_reset_complete.html'
    ), name='password_reset_complete'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)