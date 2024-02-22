from django.db.models.signals import post_save
from django.dispatch import receiver
from .utils import send_email
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import status
from decouple import config
from .models import TalentRequestTicket, PaymentTicket, DefermentTicket

User = get_user_model()

@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    if created:
        subject = "Welcome to InternPulse!"
        sender_name = "InternPulse"
        sender_email = config("EMAIL_SENDER")
        reply_to_email = config("REPLY_TO_EMAIL")
        html_content = f"""
                <html>
                <body>
                        <h3>Welcome, {instance.username}!</h3>
                        <p>You are Almost There! Kindly enter the OTP below to validate your email.</p>
                        <strong>{instance.secret}</strong>
                </body>
                </html>
            """
        to = [
            {
                "email": instance.email,
                "name": instance.username,
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
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            response_data = {
                "message": "Failed to send email. Please try again later.",
            }
            instance.delete()
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@receiver(post_save, sender=TalentRequestTicket)
def send_talent_email(sender, instance, created, **kwargs):
    if created:
        subject = "Thanks For Choosing Us!"
        sender_name = "InternPulse"
        sender_email = config("EMAIL_SENDER")
        reply_to_email = config("REPLY_TO_EMAIL")
        html_content = f"""
                <html>
                <body>
                        <h3>Hi there, {instance.company_name}!</h3>
                        <p>We received your request for {instance.talent_count} interns. Please be patient, as your request
                            is being considered. We'll get back to you shortly.
                        </p>
                        
                </body>
                </html>
            """
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
        if sent_email == "Success":
            response_data = {
                "message": f"A confirmation email has been sent to {instance.company_mail}. Please check your inbox or spam folder.",
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            response_data = {
                "message": "Failed to send email. Please try again later.",
            }
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
@receiver(post_save, sender=PaymentTicket)
def send_payment_email(sender, instance, created, **kwargs):
    if created:  
        if instance.status == "UNSUCCESSFUL":
            subject = "Payment Unsuccessful"
            message = f"Your payment of {instance.amount} for {instance.payment_reason} is unsuccessful."
        elif instance.status == "PENDING":
            subject = "Payment Pending"
            message = f"Your payment of {instance.amount} for {instance.payment_reason} is pending."
        elif instance.status == "SUCCESSFUL":
            subject = "Payment Successful"
            message = f"Your payment of {instance.amount} for {instance.payment_reason} has been successful. You will receive equivalent value for the service rendered very soon."

        sender_name = "InternPulse"
        sender_email = config("EMAIL_SENDER")
        reply_to_email = config("REPLY_TO_EMAIL")

        html_content = f"""
            <html>
            <body>
                <h3>Hello, {instance.sender_id.username}!</h3>
                <p>{message}</p>
            </body>
            </html>
        """

        to = [{"email": instance.sender_id.email, "name": instance.sender_id.username}]

        sent_email = send_email(
            to=to,
            subject=subject,
            sender={"name": sender_name, "email": sender_email},
            reply_to={"email": reply_to_email},
            html_content=html_content,
        )

        if sent_email == "Success":
            response_data = {
                "message": f"A message concerning the status of your transaction has been sent to {instance.sender_id.email}. Please check your inbox or spam folder.",
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            response_data = {
                "message": "Failed to send email. Please try again later.",
            }
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@receiver(post_save, sender=DefermentTicket)
def send_payment_email(sender, instance, created, **kwargs):
    if created:  
        if instance.status == "PENDING":
            subject = "Deferment Request In-progress"
            message = f"Your deferment request is being reviewed. We'll get back to you shortly."        

        sender_name = "InternPulse"
        sender_email = config("EMAIL_SENDER")
        reply_to_email = config("REPLY_TO_EMAIL")

        html_content = f"""
            <html>
            <body>
                <h3>Hello, {instance.sender_id.username}!</h3>
                <p>{message}</p>
            </body>
            </html>
        """

        to = [{"email": instance.sender_id.email, "name": instance.sender_id.username}]

        sent_email = send_email(
            to=to,
            subject=subject,
            sender={"name": sender_name, "email": sender_email},
            reply_to={"email": reply_to_email},
            html_content=html_content,
        )

        if sent_email == "Success":
            response_data = {
                "message": f"A message concerning the status of your deferment has been sent to {instance.sender_id.email}. Please check your inbox or spam folder.",
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            response_data = {
                "message": "Failed to send email. Please try again later.",
            }
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
