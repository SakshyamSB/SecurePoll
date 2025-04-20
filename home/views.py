from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from home.models import CustomUser

User = get_user_model()

def open_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')  # Get email from form
        password = request.POST.get('password')  # Get password from form
        
        try:
            user = CustomUser.objects.get(email=email)
            

            if user.check_password(password):  
                login(request, user)  
                return redirect('landing')  
            else:
                messages.error(request, "Invalid email or password.")
        except CustomUser.DoesNotExist:
            messages.error(request, "Invalid email or password.")

    return render(request, 'home/login.html')  



def open_registration(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        voter_id = request.POST.get('voter_id')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered.")
        elif User.objects.filter(voter_id=voter_id).exists():
            messages.error(request, "This voter ID is already taken.")
        else:
            user = User.objects.create_user(
                username=email,
                email=email,
                password=password,
                voter_id=voter_id,
                is_active=False  # Email verification required
            )
            user.first_name = first_name
            user.last_name = last_name
            user.save()

            send_verification_email(user, request)
            messages.success(request, "Registration successful! Please check your email to verify your account.")
            return redirect('login')  

    return render(request, 'home/registration.html')

def verify_email(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse("Email verified! You can now log in.")
    else:
        return HttpResponse("Invalid or expired link.")

def send_verification_email(user, request):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    domain = get_current_site(request).domain
    link = f"http://{domain}/verify-email/{uid}/{token}/"

    subject = 'Verify your Email'
    message = render_to_string('email/activation_email.html', {
        'user': user,
        'verification_link': link
    })

    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])

@login_required
def open_home(request):
    logout(request)
    if request.method == 'POST':
        logout(request)  
        messages.success(request, "You have been logged out.")
        return redirect('login')  

    return render(request, 'home/landing.html')  

        

# def open_registration(request):
#     if request.method == 'POST':
#         first_name = request.POST.get('first_name')
#         last_name = request.POST.get('last_name')
#         email = request.POST.get('email')
#         password = request.POST.get('password')
#         voter_id = request.POST.get('voter_id')  # Get the voter_id from the form

#         # Check if user with this email already exists
#         if CustomUser.objects.filter(email=email).exists():
#             messages.error(request, "Email is already registered.")
#         # Check if the provided voter_id already exists
#         elif CustomUser.objects.filter(voter_id=voter_id).exists():
#             messages.error(request, "This voter ID is already taken. Please use a different one.")
#         else:
#             # Create new user using CustomUser model
#             user = CustomUser.objects.create_user(username=email, email=email, password=password, voter_id=voter_id)
#             user.first_name = first_name
#             user.last_name = last_name
#             user.save()

#             messages.success(request, "Registration successful! You can now login.")

#     return render(request, 'home/registration.html')