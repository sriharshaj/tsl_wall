from django.core.mail import send_mail


def send_user_welcome_email(user_email):
    message = """ <h3>Welcome to The Wall</h3>
    <p>On the wall you can post your thoughts and
    express your ideas.</p>
    """
    send_mail(
        'Welcome to The Wall',
        message,
        'support@thewall.com',
        [user_email],
        fail_silently=False,
    )
