from django.core.mail import EmailMessage
from django.shortcuts import get_object_or_404
from requests import Response

from rest_framework import viewsets, filters, permissions, status

from api.serializers import (UsersSerializer,
                             CategorySerializer,
                             GenreSerializer,
                             ReviewSerializer,
                             TitleSerializer,
                             ReviewSerializer,
                             CommentSerializer)
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from reviews.models import User, Category, Genre, Title, Review, Comment

from .permissions import AdminOnly, IsAdminUserOrReadOnly, AdminModeratorAuthorPermission
from .serializers import GetTokenSerializer, NotAdminSerializer, SignUpSerializer


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    permission_classes = (IsAuthenticated, AdminOnly,)
    lookup_field = 'username'
    filter_backends = (SearchFilter,)
    search_fields = ('username',)

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

    def post(self, request):
        serializer = GetTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        try:
            user = User.objects.get(username=data['username'])
        except User.DoesNotExist:
            return Response(
                {'username': 'Пользователь с таким именем не найден!'},
                status=status.HTTP_404_NOT_FOUND)
        if data.get('confirmation_code') == user.confirmation_code:
            token = RefreshToken.for_user(user).access_token
            return Response({'token': str(token)},
                            status=status.HTTP_201_CREATED)
        return Response(
            {'confirmation_code': 'Ошибка! Неверный код подтверждения!'},
            status=status.HTTP_400_BAD_REQUEST)


class APISignup(APIView):
    """
    Получение письма с доступом для API
    """
    permission_classes = (permissions.AllowAny,)

    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject=data['email_subject'],
            body=data['email_body'],
            to=[data['to_email']]
        )
        email.send()

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        email_body = (
            f'Добрый день, {user.username}.'
            f'Ваш код доступа к API: {user.confirmation_code}'
        )
        data = {
            'email_body': email_body,
            'to_email': user.email,
            'email_subject': 'Код подтверждения доступа к API!'
        }
        self.send_email(data)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryViewSet(viewsets.ModelViewSet):
    # permission_classes = (IsAdminOrReadOnly, )
    queryset = Category.objects.all()
    permission_classes = (IsAdminUserOrReadOnly,)
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class GenreViewSet(viewsets.ModelViewSet):
    # Здесь ещё будет дополняться ViewSet жанров
    queryset = Genre.objects.all()
    permission_classes = (IsAdminUserOrReadOnly,)
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    pass


class TitleViewSet(viewsets.ModelViewSet):
    # Здесь ещё будет дополняться ViewSet произведений
    queryset = Title.objects.all()
    permission_classes = (IsAdminUserOrReadOnly,)
    serializer_class = TitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    # Здесь ещё будет дополняться ViewSet отзывов
    queryset = Review.objects.all()
    permission_classes = (AdminModeratorAuthorPermission,)
    serializer_class = ReviewSerializer

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        return title.comments.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    # Здесь ещё будет дополняться ViewSet комментов
    queryset = Comment.objects.all()
    permission_classes = (AdminModeratorAuthorPermission,)
    serializer_class = CommentSerializer

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)
