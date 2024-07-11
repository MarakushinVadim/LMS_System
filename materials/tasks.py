from celery import shared_task
from django.core.mail import send_mail

from LMS_System import settings
from materials.models import Course, Subscription


@shared_task
def check_courses(pk_course):
    course = Course.objects.filter(pk=pk_course).first()

    if course:
        subscription = Subscription.objects.filter(course=course)
        recipient_list = []
        for sub in subscription:
            recipient_list.append(sub.owner.email)
        send_mail(
            subject=f'Курс {course.name} был обновлен',
            message='Зайдите в курс чтобы посмотреть на обновления',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=recipient_list,
        )
