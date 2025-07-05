from accounts.models import AccountCode
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import (
    login as django_login,
    logout as django_logout,
    get_user_model,
)
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import Http404

from loginas.views import user_logout as la_restore

from .forms import FadderEditForm
from fadderanmalan.models import Job
from fadderanmalan.utils import misc as misc_utils

from trade.models import Trade

from util import to_student_email
import re

User = get_user_model()

# Cheap, but dumb, to check for liu IDs
# Might bite us in the ass
liu_id = re.compile(r"^[a-z]{5}[0-9]{3}$")


def login(request):
    if request.method != "POST":
        return render(request, "accounts/login.html", {"failed": False})

    username = request.POST.get("username")
    password = request.POST.get("password")

    user = authenticate(username=username, password=password)
    if user is None:
        return render(request, "accounts/login.html", {"failed": True})

    if not user.is_activated:
        return render(request, "accounts/login.html", {"failed": True, "error_message": "Användaren är inte aktiverad!"})

    django_login(request, user)
    return redirect("index")


def register(request):
    if request.method != "POST":
        return render(request, "accounts/register.html", {"failed": False})

    username = request.POST.get("username")
    password = request.POST.get("password")
    repeat_password = request.POST.get("repeat_password")

    if (not username or liu_id.match(username) is None):
        return render(request, "accounts/register.html", {"failed": True, "error_message": "Vänligen kontrolla ditt Liu-ID."})

    if (not password or not repeat_password):
        return render(request, "accounts/register.html", {"failed": True, "error_message": "Du måste fylla i ett lösenrod."})

    if (len(password) < 10):
        return render(request, "accounts/register.html", {"failed": True, "error_message": "Lösenordet måste vara minst 10 tecken långt."})

    if password != repeat_password:
        return render(request, "accounts/register.html", {"failed": True, "error_message": "Lösenorden matchar inte."})

    if User.objects.filter(username=username).exists():
        return render(request, "accounts/register.html", {"failed": True, "error_message": "En användare finns redan för detta Liu-ID."})

    user = User.objects.create_user(username=username, password=password, email=to_student_email(username))
    user.save()

    user.send_activation_email()

    return redirect("accounts:activate")


def logout(request):
    django_logout(request)
    return redirect("index")


def activate(request):
    if request.method == "GET":
        return render(request, "accounts/activate_account.html", {"failed": False})

    activation_code = request.POST.get("activation_code")
    if not activation_code:
        return render(request, "accounts/activate_account.html", {"failed": True, "error_message": "Du måste fylla i en aktiveringskod."})

    try:

        account_code = AccountCode.objects.get(code=activation_code)
        user = account_code.user
        user.is_activated = True
        user.save()
        account_code.delete()

        django_login(request, user)

        return redirect("index")
    except User.DoesNotExist:
        return render(request, "accounts/activate_account.html", {"failed": True})


def loginfailed(request):
    return render(request, "accounts/loginfailed.html")


def profile(request, username):
    if username == request.user.username:
        return render(
            request,
            "accounts/my_profile.html",
            dict(
                non_returned_equipment_ownerships=request.user.equipments.all(),
                day_grouped=Job.group_by_date(request.user.jobs.all()),
            ),
        )

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        raise Http404("Kunde inte hitta användaren '%s'" % username)

    jobs = misc_utils.filter_jobs_for_user(request.user, user.jobs)

    day_grouped = Job.group_by_date(jobs)

    if request.user.is_anonymous:
        trade = None
    else:
        try:
            trade = Trade.get_trade(request.user, user)
        except Trade.DoesNotExist:
            trade = None

    return render(
        request,
        "accounts/profile.html",
        dict(user=user, day_grouped=day_grouped, trade=trade,),
    )


def my_profile(request):
    return redirect("accounts:profile", request.user.username)


@login_required
def edit_profile(request):
    if request.method == "POST":
        form = FadderEditForm(data=request.POST)

        if form.is_valid():
            request.user.email = form.cleaned_data.get("email")

            # The "or None" part is necessary since the form will submit with empty strings, which means we
            # can't do checks like "if phone is None" (done in for example warn_no_phone_number middleware)
            request.user.phone_number = form.cleaned_data.get("phone_number") or None
            request.user.motto = form.cleaned_data.get("motto")
            request.user.name = form.cleaned_data.get("name")

            password = form.cleaned_data.get("password")
            if password != "":
                request.user.set_password(password)

            request.user.save()

            messages.add_message(
                request,
                messages.INFO,
                "Din profil har uppdaterats. "
                "<a href='%s'>Se dina ändringar.</a>" % reverse("accounts:my_profile"),
            )
        else:
            messages.add_message(
                request, messages.ERROR, "Ett eller flera problem uppstod."
            )
    else:
        form = FadderEditForm(
            initial=dict(
                email=request.user.email,
                phone_number=request.user.phone_number,
                motto=request.user.motto,
                name=request.user.name,
            )
        )

    return render(request, "accounts/edit_profile.html", dict(form=form,))


@login_required
def restore_impersonation(request):
    # Clear any messages generated by the impersonated login before switching back
    list(messages.get_messages(request))

    return la_restore(request)
