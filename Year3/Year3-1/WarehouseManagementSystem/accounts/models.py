from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    ROLE_CHOICES = [
        ("ADMIN", "管理员"),
        ("USER", "普通用户"),
    ]


    STATUS_CHOICES = [
        ("PENDING", "等待审核"),
        ("APPROVED", "已通过"),
        ("REJECTED", "已拒绝"),
        ("DISABLED","已禁用"),
    ]


    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )


    real_name = models.CharField(
        max_length=50
    )


    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default="USER"
    )


    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="PENDING"
    )

    approved_time = models.DateTimeField(
        null=True,
        blank=True
    )


    def __str__(self):
        return self.user.username