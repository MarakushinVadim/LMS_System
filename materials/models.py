from django.db import models

from LMS_System.settings import AUTH_USER_MODEL

NULLABLE = {"blank": True, "null": True}


class Course(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название курса")
    preview = models.ImageField(upload_to="media", **NULLABLE, verbose_name="Превью")
    description = models.TextField(verbose_name="Описание курса")
    owner = models.ForeignKey(
        AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE, verbose_name="Владелец"
    )
    amount = models.PositiveIntegerField(default=1000, verbose_name="Стоимость курса")
    last_update_date = models.DateTimeField(
        **NULLABLE, verbose_name="дата и время последнего обновления"
    )

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"

    def __str__(self):
        return self.name


class Lessons(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название урока")
    description = models.TextField(verbose_name="Описание урока")
    preview = models.ImageField(upload_to="media", verbose_name="Превью", **NULLABLE)
    video_link = models.CharField(max_length=255, verbose_name="Ссылка на видео")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="Курс")
    owner = models.ForeignKey(
        AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE, verbose_name="Владелец"
    )

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"

    def __str__(self):
        return self.name


class Subscription(models.Model):
    owner = models.ForeignKey(
        AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Владелец"
    )
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="Курс")
    amount = models.IntegerField(**NULLABLE, verbose_name="Цена курса")

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"

        def __str__(self):
            return f"{self.owner} - подписка на курс {self.course}"


class Amounts(models.Model):
    user = models.ForeignKey(
        AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Пользователь"
    )
    session_id = models.CharField(max_length=255, **NULLABLE, verbose_name="id сессии")
    link = models.URLField(max_length=400, **NULLABLE, verbose_name="ссылка на оплату")
    product = models.ForeignKey(
        Course, on_delete=models.CASCADE, verbose_name="Курс", **NULLABLE
    )
    amount = models.PositiveIntegerField(verbose_name="Стоимость курса", **NULLABLE)

    def __str__(self):
        return f"Платеж {self.pk}"
