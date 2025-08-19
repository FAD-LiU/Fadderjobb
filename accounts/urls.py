from django.urls import path

#import cas.views

from loginas.views import user_logout

from . import views


app_name = "accounts"

urlpatterns = [
    path("login", views.login, name="login"),
    path("register", views.register, name="register"),
    path("logout", views.logout, name="logout"),
    path("activate", views.activate, name="activate"),
    path("reset_password", views.request_password_reset, name="request_reset_password"),
    path(
        "reset_password/<str:reset_code>/", views.reset_password, name="reset_password"
    ),
    path("restore/", views.restore_impersonation, name="restore"),
    path("my_profile/", views.my_profile, name="my_profile"),
    path("edit_profile/", views.edit_profile, name="edit_profile"),
    path("profile/<str:username>", views.profile, name="profile"),
    path("loginfailed", views.loginfailed, name="loginfailed"),
]
