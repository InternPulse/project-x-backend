from django.db.models.signals import post_save
from django.dispatch import receiver
from .utils import send_email
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import status
import os


@receiver(post_save, sender=get_user_model())
def send_welcome_email(sender, instance, created, **kwargs):
    if created:
        subject = "Welcome to InternPulse!"
        sender_name = "InternPulse"
        sender_email = os.environ.get("EMAIL_SENDER")
        reply_to_email = os.environ.get("REPLY_TO_EMAIL")
#
        html_content = f"""
                <html>
                <body>
                        <h3>Welcome, {instance.first_name} {instance.last_name}!</h3>
                        <p>You are Almost There! Kindly enter the OTP below to validate your email.</p>
                        <strong>{instance.secret}</strong>
                </body>
                </html>
            """
        to = [
            {
                "email": instance.email,
                "name": f"{instance.first_name}, {instance.last_name}",
            }
        ]
        sent_email = send_email(
            to=to,
            subject=subject,
            sender={"name": sender_name, "email": sender_email},
            reply_to={"email": reply_to_email},
            html_content=html_content,
        )
        if sent_email == "Success":
            response_data = {
                "message": f"Enter the OTP that has been sent to {instance.email}. Please check your inbox or spam folder.",
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            response_data = {
                "message": "Failed to send email. Please try again later.",
            }
            instance.delete()
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
