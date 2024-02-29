from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from .utils import send_email
from django.contrib.auth import get_user_model
from decouple import config
from .models import TalentRequestTicket
from user_management.signals import password_reset, verification
import utils.otp as u
from django.conf import settings

User = get_user_model()


@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    if created and not (instance.is_staff and instance.is_superuser):
        subject = "Welcome to InternPulse!"
        sender_name = "InternPulse"
        sender_email = config("EMAIL_SENDER")
        reply_to_email = config("REPLY_TO_EMAIL")
        html_content = render_to_string(
            "welcome_email.html",
            {
                "full_name": instance.full_name,
                "otp": u.get_otp(instance),
            },
        )
        to = [
            {
                "email": instance.email,
                "name": instance.full_name,
            }
        ]
        sent_email = send_email(
            to=to,
            subject=subject,
            sender={"name": sender_name, "email": sender_email},
            reply_to={"email": reply_to_email},
            html_content=html_content,
        )
        if not sent_email == "Success":
            instance.delete()


@receiver(post_save, sender=TalentRequestTicket)
def send_talent_email(sender, instance, created, **kwargs):
    if created:
        subject = "Thanks For Choosing Us!"
        sender_name = "InternPulse"
        sender_email = config("EMAIL_SENDER")
        reply_to_email = config("REPLY_TO_EMAIL")
        html_content = render_to_string(
            "talent_request_email.html", {"company_name": instance.company_name}
        )
        to = [
            {
                "email": instance.company_mail,
                "name": instance.company_name,
            }
        ]
        sent_email = send_email(
            to=to,
            subject=subject,
            sender={"name": sender_name, "email": sender_email},
            reply_to={"email": reply_to_email},
            html_content=html_content,
        )
    return sent_email == "Success" 

@receiver(password_reset)
def password_reset_receiver(sender, **kwargs):
    user = kwargs.get("user")
    if user:
        token = u.generate_otp_link(user.id, "pwd")
        link = f"{settings.FE_URL}/password-reset/{token}"
        subject = "Reset your password"
        sender_name = "InternPulse"
        sender_email = config("EMAIL_SENDER")
        reply_to_email = config("REPLY_TO_EMAIL")
        html_content = render_to_string(
            "password_reset_email.html", {"full_name": user.full_name, "link": link}
        )
        to = [
            {
                "email": user.email,
                "name": user.full_name,
            }
        ]
        sent_email = send_email(
            to=to,
            subject=subject,
            sender={"name": sender_name, "email": sender_email},
            reply_to={"email": reply_to_email},
            html_content=html_content,
        )
    return sent_email == "Success"


@receiver(verification)
def verification_receiver(sender, **kwargs):
    user = kwargs.get("user")
    if user:
        subject = "Verify your account"
        sender_name = "InternPulse"
        sender_email = config("EMAIL_SENDER")
        reply_to_email = config("REPLY_TO_EMAIL")
        html_content = render_to_string(
            "otp_verification_email.html",
            {"full_name": user.full_name, "otp": u.get_otp(user)},
        )
        to = [
            {
                "email": user.email,
                "name": user.full_name,
            }
        ]
        sent_email = send_email(
            to=to,
            subject=subject,
            sender={"name": sender_name, "email": sender_email},
            reply_to={"email": reply_to_email},
            html_content=html_content,
        )
    return sent_email == "Success"
