import datetime as dt

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

    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True
    )

    class Meta:
        model = Title
        fields = '__all__'

    def validate_title_year(self, year):
        now = dt.date.today().year
        if year > now:
            raise serializers.ValidationError(
                'Год выпуска не может быть больше текущего!'
            )
        return year


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
