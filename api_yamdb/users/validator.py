import re

from django.conf import settings

from rest_framework import serializers


def validate_username(data):
    if data == settings.NAME_ME:
        raise serializers.ValidationError(
            'Имя пользователя "me" недопустимо'
        )
    if bool(re.fullmatch(r'^[\w.@+-]+', data)) is False:
        raise serializers.ValidationError(
            'Имя пользователя не соответствует шаблону'
        )
    return data
