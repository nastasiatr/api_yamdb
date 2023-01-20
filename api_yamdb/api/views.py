from django.shortcuts import get_object_or_404

from rest_framework import viewsets

from api.serializers import (UsersSerializer,
                             CategorySerializer,
                             GenreSerializer,
                             ReviewSerializer,
                             TitleSerializer,
                             ReviewSerializer,
                             CommentSerializer)

from reviews.models import User, Category, Genre, Title, Review, Comment


class UsersViewSet(viewsets.ModelViewSet):
    # Здесь ещё будет дополняться ViewSet пользователей

    queryset = User.objects.all()
    serializer_class = UsersSerializer
    pass


class CategoryViewSet(viewsets.ModelViewSet):
    # Здесь ещё будет дополняться ViewSet категорий

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pass


class GenreViewSet(viewsets.ModelViewSet):
    # Здесь ещё будет дополняться ViewSet жанров

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pass


class TitleViewSet(viewsets.ModelViewSet):
    # Здесь ещё будет дополняться ViewSet произведений

    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    pass


class ReviewViewSet(viewsets.ModelViewSet):
    # Здесь ещё будет дополняться ViewSet отзывов

    queryset = Review.objects.all()
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
    serializer_class = CommentSerializer
    
    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)
