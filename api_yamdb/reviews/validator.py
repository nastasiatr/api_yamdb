from django.utils import timezone
from rest_framework import serializers


def validate_title_year(year):
    now = timezone.now().year
    if year > now:
        raise serializers.ValidationError(
            'Год выпуска не может быть больше текущего!'
        )
    return year
