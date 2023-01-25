from django.contrib.auth.models import AbstractUser
from django.contrib.auth.tokens import default_token_generator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

USER = 'user'
ADMIN = 'admin'
MODERATOR = 'moderator'

ROLE_CHOICES = [
    ('user', USER),
    ('admin', ADMIN),
    ('moderator', MODERATOR),
]


class User(AbstractUser):
    username = models.CharField(
        verbose_name='Nickname',
        max_length=150,
        unique=True
    )
    email = models.EmailField(
        verbose_name='Email',
        max_length=254,
        unique=True
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=150,
        blank=True,
        null=True
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=150,
        blank=True,
        null=True
    )
    bio = models.TextField(
        verbose_name='Биография',
        blank=True,
        null=True
    )
    role = models.CharField(
        verbose_name='Роль',
        default='user',
        max_length=30, 
        blank=True
    )
    confirmation_code = models.CharField(
        verbose_name='Код подтверждения',
        max_length=8,
        blank=True,
        null=True,
        default='00000000'
    )

    @property
    def is_user(self):
        return self.role == USER

    @property
    def is_admin(self):
        return self.role == ADMIN

    @property
    def is_moderator(self):
        return self.role == MODERATOR

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class Category(models.Model):
    name = models.CharField(
        verbose_name='Название категории',
        max_length=256,
        unique=True
    )
    slug = models.SlugField(
        verbose_name='Slug категории',
        max_length=50,
        unique=True
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self) -> str:
        return self.slug


class Genre(models.Model):
    name = models.CharField(
        verbose_name='Название жанра',
        max_length=256,
        unique=True
    )
    slug = models.SlugField(
        verbose_name='Slug жанра',
        max_length=50,
        unique=True
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self) -> str:
        return self.slug


class Title(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=256
    )
    year = models.IntegerField(
        verbose_name='Год выпуска'
    )
    description = models.TextField(
        verbose_name='Описание',
        blank=True,
        null=True
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='genre_title',
        verbose_name='Жанр'
    )
    category = models.ForeignKey(
        Category,
        related_name='category_title',
        verbose_name='Категория',
        on_delete=models.SET_NULL,
        null=True
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self) -> str:
        return self.name


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='review_title',
        verbose_name='Произведение'
    )
    text = models.TextField(
        verbose_name='Текст отзыва'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='review_author',
        verbose_name='Aвтор отзыва'
    )
    score = models.IntegerField(
        verbose_name='Оценка',
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return self.text


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comment_review',
        verbose_name='Отзыв'
    )
    text = models.CharField(
        verbose_name='Текст комментария',
        max_length=400
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comment_author',
        verbose_name='Автор комментария'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text
