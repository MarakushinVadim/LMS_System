import datetime

import pytz
from celery import shared_task

from users.models import User


@shared_task
def check_last_login():
    currency = datetime.datetime.now(pytz.timezone("Europe/Moscow")).replace(
        tzinfo=pytz.timezone("Europe/Moscow")
    )
    users = User.objects.filter(is_active=True).all()
    for user in users:
        user_last_login = user.last_login
        if user_last_login is not None:
            if currency - user_last_login > datetime.timedelta(weeks=4):
                user.is_active = False
                user.save()
