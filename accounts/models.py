from datetime import datetime

from fadderjobb.utils import notify_user

from django.conf import settings
from django.shortcuts import reverse
from django.db import models
from django.db.models import Sum
from django.utils import timezone
from django.contrib.auth.models import AbstractUser, UserManager
from django.contrib.sessions.models import Session
from django.utils.crypto import get_random_string

from phonenumber_field.modelfields import PhoneNumberField

from util import to_student_email
from fadderjobb.settings_shared import PUBLIC_HOST

class _UserManager(UserManager):
    def get_by_natural_key(self, username):
        case_insensitive_username_field = "{}__iexact".format(self.model.USERNAME_FIELD)
        return self.get(**{case_insensitive_username_field: username})


class BonusPoints(models.Model):
    reason = models.CharField(max_length=100)
    points = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.reason


class User(AbstractUser):
    objects = _UserManager()

    motto = models.TextField(max_length=100, blank=True)
    phone_number = PhoneNumberField(blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    read_guide = models.BooleanField(default=False)

    points = models.IntegerField(default=0)
    placing = models.IntegerField(blank=True, null=True)
    bonus_points = models.ManyToManyField(BonusPoints, blank=True)

    is_activated = models.BooleanField(default=False)
    activation_key = models.CharField(max_length=100, blank=True)

    def __str__(self):
        if self.name:
            return "%s (%s)" % (self.name, self.username)
        return self.username

    def update_points(self):
        job_points = self.jobs.all().aggregate(Sum("points"))["points__sum"] or 0
        bonus_points = (
            self.bonus_points.all().aggregate(Sum("points"))["points__sum"] or 0
        )
        self.points = job_points + bonus_points
        self.save()

    def can_register(self):
        if self.is_superuser or self.is_staff:
            return True

        return (
            self.is_authenticated and self.phone_number is not None and self.read_guide
        )

    def get_active_received_trades(self):
        return self.received_trades.filter(completed=False).all()

    def get_active_sent_trades(self):
        return self.sent_trades.filter(completed=False).all()

    def local_url(self):
        if not self.username:
            return None
        return reverse("accounts:profile", args=[self.username])

    def url(self):
        local_url = self.local_url()

        if not local_url:
            return None
        return settings.DEFAULT_DOMAIN + local_url

    def send_activation_email(self):
        if self.is_activated:
            return

        if not self.email:
            self.email = to_student_email(self.username)

        self.activation_key = get_random_string(length=100)
        self.save()

        notify_user(
            self,
            template="accounts/email/activate_account",
            template_context=dict(activation_code=self.activation_key),
        )