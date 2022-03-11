from django.contrib.auth.models import AbstractUser
from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=100, unique=True)


class CustomUser(AbstractUser):
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, blank=False, null=False
    )
    email = models.EmailField(unique=True)


class Log(models.Model):
    TYPES = (
        ("login", "login"),
        ("logout", "logout"),
    )

    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, blank=True, null=True
    )
    log_type = models.CharField(max_length=10, choices=TYPES)
    created_at = models.DateTimeField(auto_now_add=True)
