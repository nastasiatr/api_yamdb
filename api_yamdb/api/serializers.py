from rest_framework import serializers

from reviews.models import User, Category, Genre, Title, Review, Comment


class UsersSerializer(serializers.ModelSerializer):
    # Здесь ещё будет дополняться Serializer пользователей

    class Meta:
        model = User
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = '__all__'


class TitleSerializer(serializers.ModelSerializer):
    # Здесь ещё будет дополняться Serializer произведений

    class Meta:
        model = Title
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    # Здесь ещё будет дополняться Serializer отзывов

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Review
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    # Здесь ещё будет дополняться Serializer комментариев

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = '__all__'
