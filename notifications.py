from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives

def notify_users_about_election(election):
    User = get_user_model()
    subject = " "

    # Render HTML message
    html_message = render_to_string('email/election_notification.html', {'election': election})

    recipient_list = list(User.objects.filter(is_active=True).values_list('email', flat=True))

    for email in recipient_list:
        msg = EmailMultiAlternatives(subject, '', settings.DEFAULT_FROM_EMAIL, [email])
        msg.attach_alternative(html_message, "text/html")
        msg.send(fail_silently=False)
