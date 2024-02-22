import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
import os


def send_email(to, reply_to, html_content, sender, subject):
    try:
        configuration = sib_api_v3_sdk.Configuration()
        configuration.api_key["api-key"] = os.environ.get("EMAIL_API_KEY")
        api_instance = sib_api_v3_sdk.TransactionalEmailsApi(
            sib_api_v3_sdk.ApiClient(configuration)
        )
        send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
            to=to,
            reply_to=reply_to,
            html_content=html_content,
            sender=sender,
            subject=subject,
        )
        api_response = api_instance.send_transac_email(send_smtp_email)

        print("Email sent successfully:", api_response)

        return "Success"

    except ApiException as e:
        print("Exception when calling SMTPApi->send_transac_email:", e)
        return "Fail"
