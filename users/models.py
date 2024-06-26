from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {"blank": True, "null": True}


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name="email")
    phone = models.CharField(max_length=35, verbose_name="phone", **NULLABLE)
    city = models.CharField(max_length=58, verbose_name="city", **NULLABLE)
    avatar = models.ImageField(
        upload_to="media/users_avatars", **NULLABLE, verbose_name="avatar"
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"

    def __str__(self):
        return self.email
