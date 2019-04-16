"""fadderjobb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, reverse_lazy
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

import cas.views


admin.autodiscover()


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("fadderanmalan.urls")),
    path('accounts/', include("accounts.urls")),

    # Going to /admin when not logged in results in a redirect to cas.views.login, which I can't be bothered to
    # find where it's configured. Adding the following line allows me to configure a non-namespaced "cas.views.login"
    # path which I can redirect to the same login-view as normal.
    # Meaning: You should _not_ use this path for reversing. If a reverse for loggin in is needed, use the one
    # configured in the accounts app.
    path('accounts/login', cas.views.login, name="cas.views.login"),

    path('calendar/', include("job_calendar.urls")),
    path('trade/', include("trade.urls")),
]

urlpatterns += staticfiles_urlpatterns()
