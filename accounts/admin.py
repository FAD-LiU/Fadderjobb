import random
import string
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.apps import apps
from django.contrib.admin.filters import BooleanFieldListFilter
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.utils.html import format_html
from django.urls import reverse
from django.db import models

from fadderjobb.utils import notify_user
from loginas.utils import login_as

from .models import BonusPoints, AccountCode
from fadderanmalan.models import EquipmentOwnership, EnterQueue
from fadderjobb.filters import DropdownFilterRelated


User = get_user_model()


def make_activated(modeladmin, request, queryset):
    """Action for marking selected users as activate through admin panel"""
    queryset.update(is_activated=True)


make_activated.short_description = "Activate selected users"


def reset_password(modeladmin, request, queryset):
    available_characters = string.ascii_letters + string.digits

    for user in queryset:
        new_password = "".join(
            random.SystemRandom().choices(available_characters, k=20)
        )
        user.set_password(new_password)
        user.save()

        notify_user(
            user,
            template="admin/accounts/email/password_reset",
            template_context=dict(
                new_password=new_password,
            ),
        )


reset_password.short_description = "Reset password"


class JobsInline(admin.TabularInline):
    verbose_name = "Job"
    verbose_name_plural = "Jobs"

    model = User.jobs.through

    fields = ("job",)

    autocomplete_fields = ("job",)

    extra = 0


class EQInline(admin.TabularInline):
    verbose_name = "Enterqueue"
    verbose_name_plural = "EnterQueue"

    model = EnterQueue

    autocomplete_fields = ("job",)

    extra = 0


class EquipmentOwnershipInline(admin.TabularInline):
    verbose_name = "Dispensed Equipment"
    verbose_name_plural = "Dispensed Equipment"

    model = EquipmentOwnership

    extra = 0

    readonly_fields = ("dispensed_at",)

    autocomplete_fields = ("job", "equipment")

    show_change_link = True


class BonusPointsAdmin(admin.ModelAdmin):
    model = BonusPoints

    fields = ("reason", "points", "created")
    readonly_fields = ("created",)


class UserAdmin(admin.ModelAdmin):
    model = User
    actions = [reset_password, make_activated]

    exclude = ("password", "first_name", "last_name", "is_active")

    fields = (
        "url",
        "username",
        "is_activated",
        "name",
        "email",
        "phone_number",
        "motto",
        "read_guide",
        "bonus_points",
        "is_superuser",
        "is_staff",
        "groups",
        "user_permissions",
        "date_joined",
        "last_login",
    )
    filter_horizontal = ("bonus_points",)

    readonly_fields = ("date_joined", "last_login", "url")

    inlines = (
        JobsInline,
        EquipmentOwnershipInline,
        EQInline,
    )

    list_display = ("username", "name", "email", "is_activated", "points", "equipment")

    search_fields = ("username", "name")

    list_filter = [
        ("is_superuser", BooleanFieldListFilter),
        ("jobs", DropdownFilterRelated),
        ("equipments__equipment", DropdownFilterRelated),
        ("groups", DropdownFilterRelated),
    ]

    def get_ordering(self, request):
        return ["username"]

    def url(self, obj):
        url = obj.url()

        if not url:
            return ""
        return format_html("<a href='{url}'>{url}</a>", url=obj.url())

    url.short_description = "URL"

    def equipment(self, obj):
        return ", ".join(str(eq.equipment) for eq in obj.equipments.all())

    def response_change(self, request, obj):
        if "_loginas" in request.POST:
            if not request.user.is_superuser:
                return HttpResponseForbidden()
            login_as(obj, request)

            return HttpResponseRedirect(reverse("index"))
        return super().response_change(request, obj)


class AccountCodeAdmin(admin.ModelAdmin):
    model = apps.get_model("accounts", "AccountCode")
    fields = ("code", "user", "type", "created")
    readonly_fields = ("created",)
    list_display = ("code", "user", "type", "created")
    search_fields = ("code", "user__username", "user__name")

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("user")


admin.site.register(User, UserAdmin)
admin.site.register(BonusPoints, BonusPointsAdmin)
admin.site.register(AccountCode, AccountCodeAdmin)
