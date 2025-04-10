from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from home.models import CustomUser
from django.contrib.auth.decorators import login_required

def open_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')  # Get email from form
        password = request.POST.get('password')  # Get password from form
        
        try:
            # Check if user with this email exists
            user = CustomUser.objects.get(email=email)
            
            # Check if the password is correct
            if user.check_password(password):  # Check hashed password
                login(request, user)  # Log in user
                return redirect('landing')  # Redirect to home page after login
            else:
                messages.error(request, "Invalid email or password.")
        except CustomUser.DoesNotExist:
            messages.error(request, "Invalid email or password.")

    return render(request, 'home/login.html')  # Render login page 



def open_registration(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        voter_id = request.POST.get('voter_id')  # Get the voter_id from the form

        # Check if user with this email already exists
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered.")
        # Check if the provided voter_id already exists
        elif CustomUser.objects.filter(voter_id=voter_id).exists():
            messages.error(request, "This voter ID is already taken. Please use a different one.")
        else:
            # Create new user using CustomUser model
            user = CustomUser.objects.create_user(username=email, email=email, password=password, voter_id=voter_id)
            user.first_name = first_name
            user.last_name = last_name
            user.save()

            messages.success(request, "Registration successful! You can now login.")

    return render(request, 'home/registration.html')

@login_required
def open_home(request):
    logout(request)
    if request.method == 'POST':
        logout(request)  # Log out the user if POST request is made (when logout button is pressed)
        messages.success(request, "You have been logged out.")
        return redirect('login')  # Redirect to the login page after logout

    return render(request, 'home/landing.html')  # Render the landing page if GET request is made

        

