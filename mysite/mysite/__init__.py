from django.core.mail import send_mail

send_mail(
    'Subject here',
    'Here is the message.',
    'missvegastop@gmail.com',
    ['100palavr@gmail.com'],
    fail_silently=False,
)