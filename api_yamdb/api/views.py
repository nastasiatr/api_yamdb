from django.shortcuts import get_object_or_404

from rest_framework import viewsets

from reviews.models import User, Category, Genre, Title, Review, Comment


class UsersViewSet(viewsets.ModelViewSet):
    # Здесь будет ViewSet пользователей
    pass


class CategoryViewSet(viewsets.ModelViewSet):
    # Здесь будет ViewSet категорий
    pass


class GenreViewSet(viewsets.ModelViewSet):
    # Здесь будет ViewSet жанров
    pass


class TitleViewSet(viewsets.ModelViewSet):
    # Здесь будет ViewSet произведений
    pass


class ReviewViewSet(viewsets.ModelViewSet):
    # Здесь будет ViewSet отзывов
    pass


class CommentViewSet(viewsets.ModelViewSet):
    # Здесь будет ViewSet комментов
    pass
