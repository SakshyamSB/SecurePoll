from django.shortcuts import get_object_or_404, render, redirect
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
from home.models import CustomUser, Election, Candidate, Vote
from django.contrib.messages import get_messages
from django.utils import timezone
from django.db.models import Count
from django.core.mail import EmailMultiAlternatives

User = get_user_model()


# @login_required
# def update_info(request):
#     if request.method == 'POST':
#         user = request.user
#         user.username = request.POST.get('username')
#         user.email = request.POST.get('email')
#         user.save()
#         get_messages.success(request, 'Information updated successfully!')
#         return redirect('my_info')  # or any page you want
#     return render(request, 'edit_info.html')


def open_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        storage = get_messages(request)
        for _ in storage:
            pass
        # Only attempt login if email is provided
        if email:
            try:
                user = CustomUser.objects.get(email=email)

                if user.check_password(password):
                    login(request, user)
                    return redirect('landing')
                else:
                    messages.error(request, "Invalid email or password.")
                    user = None
            except CustomUser.DoesNotExist:
                messages.error(request, "Invalid email or password.")
                user = None
        return redirect('login')  
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

    # Render HTML content
    html_message = render_to_string('email/activation_email.html', {
        'user': user,
        'verification_link': link
    })

    msg = EmailMultiAlternatives(
        subject=subject,
        body='',  # Empty or use plain_message if available
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[user.email]
    )
    msg.attach_alternative(html_message, "text/html")
    msg.send(fail_silently=False)

@login_required
def open_home(request):
    if request.method == 'POST':
        logout(request)  
        messages.success(request, "You have been logged out.")
        return redirect('login')  

    return render(request, 'home/landing.html')  

        

def cast_vote(request):
    elections = Election.objects.filter(start_date__lte=timezone.now(), end_date__gte=timezone.now())

    if request.method == 'POST':
        for election in elections:
            candidate_id = request.POST.get(f"candidate_{election.id}")
            if candidate_id:
                candidate = Candidate.objects.get(id=candidate_id)
                # Check if already voted
                if not Vote.objects.filter(voter=request.user, election=election).exists():
                    Vote.objects.create(
                        voter=request.user,
                        candidate=candidate,
                        election=election
                    )
        messages.success(request, "Your vote has been submitted.")
        return redirect('landing')

    return render(request, 'home/vote.html', {'elections': elections})



@login_required
def submit_vote(request, election_id):
    election = get_object_or_404(Election, pk=election_id)
    if Vote.objects.filter(voter=request.user, election=election).exists():
        messages.error(request, "You have already voted in this election.")
        return redirect('cast_vote')

    if request.method == 'POST':
        candidate_id = request.POST.get('candidate_id')
        candidate = get_object_or_404(Candidate, pk=candidate_id, election=election)

        Vote.objects.create(
            voter=request.user,
            candidate=candidate,
            election=election
        )
        messages.success(request, "Your vote has been cast successfully.")
        return redirect('cast_vote')



@login_required
def my_info(request):
    user = request.user  # Get the logged-in user
    return render(request, 'my_info.html', {'user': request.user})


def user_logout(request):
    logout(request)  # Django's built-in logout function
    messages.success(request, "You have been logged out successfully.")
    return redirect('login')  # Redirect to login page after logging out



@login_required
def election_results(request):
    finished_elections = Election.objects.filter(end_date__lt=timezone.now())
    results = []

    for election in finished_elections:
        candidates_qs = election.candidates.annotate(vote_count=Count('vote')).order_by('-vote_count')
        total_votes = sum(c.vote_count for c in candidates_qs)

        total_candidates = candidates_qs.count()
        turnout_percent = (total_votes / total_candidates) * 100 if total_candidates > 0 else 0

        candidates = []
        for c in candidates_qs:
            vote_percent = (c.vote_count / total_votes) * 100 if total_votes > 0 else 0
            candidates.append({
                'full_name': c.full_name,
                'party_name': c.party_name,
                'vote_count': c.vote_count,
                'vote_percent': round(vote_percent, 1),
            })

        results.append({
            'election': election,
            'candidates': candidates,
            'total_votes': total_votes,
            'total_candidates': total_candidates,
            'turnout_percent': round(turnout_percent, 1),
        })

    return render(request, 'home/election_results.html', {'results': results})

