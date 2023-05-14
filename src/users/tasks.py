from typing import Any
from uuid import UUID

from celery import shared_task
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


@shared_task
def send_email_message(subject: str, template_name: str, user_id: UUID, ctx: dict[str, Any]) -> None:
    """Send email to users."""
    html_message = render_to_string(template_name, ctx)
    plain_message = strip_tags(html_message)
    send_mail(
        subject=subject,
        message=plain_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[get_user_model().objects.get(id=user_id).email],
        fail_silently=False,
        html_message=html_message,
    )
