import re

from rest_framework import serializers


def validate_username(data):
    if data == 'me':
        raise serializers.ValidationError(
            'Имя пользователя "me" недопустимо'
        )
    if bool(re.fullmatch(r'^[\w.@+-]+', data)) is False:
        raise serializers.ValidationError(
            'Имя пользователя не соответствует шаблону'
        )
    return data
