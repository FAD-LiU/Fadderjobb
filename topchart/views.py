from django.shortcuts import render

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import F

User = get_user_model()


@login_required
def index(request):
    search = request.GET.get("search", "")

    admin = request.user and request.user.is_staff

    users = User.objects.order_by(F("placing")).all()

    if search != "":
        name_filtered = users.filter(name__icontains=search)
        username_filtered = users.filter(username__icontains=search)
        users = name_filtered.union(username_filtered)

    if not admin:
        users = users.filter(points__gt=0)[:20]

    return render(
        request, "topchart/index.html", dict(users=users, filter_search=search)
    )
