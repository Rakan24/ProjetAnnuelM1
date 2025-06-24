from django.core.mail import send_mail
from django.conf import settings

def send_email(to_email, subject, message, html_message=None):
    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [to_email],
            fail_silently=False,
            html_message=html_message
        )
        print(f"📧 Email envoyé à {to_email}")
    except Exception as e:
        print(f"❌ Erreur d'envoi d'e-mail : {e}")
