from django.contrib import admin

from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "real_name",
        "role",
        "status",
    )


    list_editable = (
        "role",
        "status",
    )