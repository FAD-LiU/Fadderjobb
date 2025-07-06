from django.template import Template, Context
from django.template.loader import get_template
from django.contrib.auth.models import Group

from post_office import mail


def send_mail(recipient, subject, message, html_message):
    mail.send(
        recipient,
        "STABEN NOREPLY <noreply@staben.info>",
        subject="Fadderjobb - " + subject,
        message=message,
        html_message=html_message,
    )


def _build_message(template_name, template_context):
    subject_template = get_template(f"{template_name}.subject.txt")
    text_template = get_template(f"{template_name}.txt")
    html_template = get_template(f"{template_name}.html")

    context = template_context or {}

    subject_rendered = subject_template.render(context).rstrip()
    text_rendered = text_template.render(context).rstrip()
    html_rendered = html_template.render(context).rstrip()

    return subject_rendered, text_rendered, html_rendered


def notify_user(
    user,
    subject=None,
    message=None,
    html_message=None,
    template=None,
    template_context=None,
):
    if template is not None:
        subject, message, html_message = _build_message(template, template_context)
    elif subject is None:
        raise Exception(
            "Neither subject nor template supplied. "
            "If not using a template, you should also include a message."
        )

    send_mail(user.email, subject, message, html_message)


def notify_group(
    group_name,
    subject=None,
    message=None,
    html_message=None,
    template=None,
    template_context=None,
):
    if template is not None:
        subject, message, html_message = _build_message(template, template_context)
    elif subject is None:
        raise Exception(
            "Neither subject nor template supplied. "
            "If not using a template, you should also include a message."
        )

    users = Group.objects.get(name=group_name).user_set.all()

    for user in users:
        send_mail(user.email, subject, message, html_message)
