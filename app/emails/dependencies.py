from app.emails.services import EmailService
from app.emails.services import EmailServiceSecure


def get_email_service():
    return EmailService()


def get_email_service_secure():
    return EmailServiceSecure()
