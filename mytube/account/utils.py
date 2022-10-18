import os
from django.core.mail import EmailMessage
from rest_framework_simplejwt.tokens import RefreshToken

class Util:
    @staticmethod
    def send_email(data):
        """send password reset email

        Args:
            data (dict): data abot email
        """
        email = EmailMessage(
            subject=data['subject'],
            body=data['body'],
            from_email=str(os.getenv('EMAIL_FROM')) ,
            to=[data['to_email']]
        )
        email.send()

def get_tokens_for_user(user):
    """Get JWT token for user, manually

    Args:
        user (object): current user data

    Returns:
        string: token
    """
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }