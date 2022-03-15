from django.core.mail import send_mail
from celery import shared_task
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.translation import gettext_lazy as _


@shared_task(name="generic_email_sender")
def generic_email_sender(subject, message, recipient, html_context=None):
    email_data = {
        "subject": subject,
        "message": message,
        "from_email": settings.DEFAULT_FROM_EMAIL,
        "recipient_list": recipient,
    }
    html_context['footer_message'] = _("If you are having trouble with the button above, copy and paste the URL below into your web browser.") # noqa E501]
    if html_context:
        email_data["html_message"] = render_to_string(
            "emails/generic_email.html", html_context
        )
    send_mail(**email_data)
