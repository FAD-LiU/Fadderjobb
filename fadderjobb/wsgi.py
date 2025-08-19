"""
WSGI config for fadderjobb project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fadderjobb.settings_production")

application = get_wsgi_application()

try:
    import uwsgidecorators
    from django.core.management import call_command

    @uwsgidecorators.timer(10)
    def send_queued_mail(num):
        """Send queued mail every 10 seconds"""
        call_command("send_queued_mail", processes=1)

    @uwsgidecorators.cron(0, 0, -1, -1, -1)
    def clear_old(num):
        """Clear old emails every day at 00:00"""
        call_command("cleanup_mail", "--days=30", "--delete-attachments")

    def clear_old_account_codes(num):
        """Clear old account codes every day at 00:00"""
        call_command("clearoldaccountcodes", "--days=30", "--delete-attachments")

except ImportError:
    print("uwsgidecorators not found. Cron and timers are disabled")
