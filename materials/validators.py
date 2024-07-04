from rest_framework.serializers import ValidationError

valid_url = "www.youtube.com"


def validate_url(url):
    if valid_url not in url.lower():
        raise ValidationError("Введен неправильный url")
