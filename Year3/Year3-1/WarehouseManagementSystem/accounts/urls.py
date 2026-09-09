
from django.urls import path
from . import views


urlpatterns = [
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("approve/",views.approve_users,name="approve_users"),
    path(
        "approve/<str:username>/",
        views.approve_user,
        name="approve_user"
    ),
    path(
        "reject/<str:username>/",
        views.reject_user,
        name="reject_user"
    ),

    path(
        "disable_user/<str:username>/",
        views.disable_user,
        name="disable_user"
    ),


    path(
        "enable_user/<str:username>/",
        views.enable_user,
        name="enable_user"
    ),

    path(
        "change_role/<str:username>/",
        views.change_role,
        name="change_role"
    ),
]