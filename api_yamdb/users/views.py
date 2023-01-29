from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404

from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.templatetags.rest_framework import data
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework.response import Response
from rest_framework import viewsets, filters, permissions, status

from users.serializers import (UsersSerializer,
                               GetTokenSerializer,
                               NotAdminSerializer,
                               SignUpSerializer)
from api.permissions import AdminOnly

from users.models import User


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    permission_classes = (IsAuthenticated, AdminOnly,)
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    http_method_names = [
        'get',
        'post',
        'patch',
        'delete'
    ]

    @action(
        methods=['GET', 'PATCH'],
        detail=False,
        permission_classes=(IsAuthenticated,),
        url_path='me')
    def get_current_user_info(self, request):
        serializer = UsersSerializer(request.user)
        if request.method == 'PATCH':
            if request.user.is_admin:
                serializer = UsersSerializer(
                    request.user,
                    data=request.data,
                    partial=True)
            else:
                serializer = NotAdminSerializer(
                    request.user,
                    data=request.data,
                    partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.data)


class APIGetToken(APIView):
    """
    Получение JWT-токена/ Адрес: 'v1/auth/token/'
    """

    def send_email(user):
        confirmation_code = default_token_generator.make_token(user)
        subject = 'Код подтверждения'
        message = f'{confirmation_code} - ваш код для авторизации'
        admin_email = 'test@test.ru'
        user_email = [user.email]
        return send_mail(subject, message, admin_email, user_email)

    def post(self, request):
        user = User.objects.filter(
            username=request.data.get('username'),
            email=request.data.get('email')
        ).first()
        if user:
            send_mail(data)
            return Response(
                'Код подтверждения отправлен вам на почту.',
                status=status.HTTP_200_OK)
        serializer = GetTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = serializer.validated_data['username']
            code = serializer.data['confirmation_code']
        except User.DoesNotExist:
            return Response(
                {'username': 'Пользователь с таким именем не найден!'},
                status=status.HTTP_404_NOT_FOUND)
        user = get_object_or_404(User, username=user)
        if code == user.confirmation_code:
            token = RefreshToken.for_user(user).access_token
            return Response(
                {'token': str(token)},
                status=status.HTTP_200_OK)
        return Response(
            {'confirmation_code': 'Ошибка! Неверный код подтверждения!'},
            status=status.HTTP_400_BAD_REQUEST)


class APISignup(APIView):
    """
    Получение письма с доступом для API
    """
    permission_classes = (permissions.AllowAny,)

    @staticmethod
    def send_email(user):
        confirmation_code = default_token_generator.make_token(user)
        subject = 'Код подтверждения'
        message = f'{confirmation_code} - ваш код для авторизации'
        admin_email = 'test@test.ru'
        user_email = [user.email]
        return send_mail(subject, message, admin_email, user_email)

    def post(self, request):
        user = User.objects.filter(
            username=request.data.get('username'),
            email=request.data.get('email')
        ).first()
        if user:
            self.send_email(user)
            return Response(
                'Код отправлен на почту.', status=status.HTTP_200_OK)

        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        self.send_email(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
            headers=headers
        )
