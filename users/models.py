from django.contrib.auth.models import AbstractUser
from django.db import models

from materials.models import Course, Lessons

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


class Payments(models.Model):
    class PayChoises(models.TextChoices):
        NAL = "NAL", "Наличные"
        TRANSFER = "TRANSFER", "Перевод"

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Пользователь"
    )
    payment_data = models.DateField(auto_now_add=True, verbose_name="Дата оплаты")
    payd_course = models.ForeignKey(
        Course, on_delete=models.CASCADE, verbose_name="оплаченный курс", **NULLABLE
    )
    payd_lessons = models.ForeignKey(
        Lessons, on_delete=models.CASCADE, verbose_name="оплаченный урок", **NULLABLE
    )
    pay_summ = models.IntegerField(verbose_name="Оплаченная сумма")
    payment_type = models.CharField(
        max_length=10, choices=PayChoises.choices, verbose_name="Тип оплаты"
    )

    class Meta:
        verbose_name = "платеж"
        verbose_name_plural = "платежи"

    def __str__(self):
        return f"{self.user} - оплаченный курс({self.payd_course}), оплаченый урок - ({self.payd_lessons})"
