from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = models.CharField(        # Сюда кажется нужно прикрутить валидатор  
        verbose_name='Nickname',
        max_length=150,
        unique=True,
        blank=False
    )
    email = models.EmailField(
        verbose_name='Email',
        max_length=254,
        unique=True,
        blank=False
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
    role = models.CharField(    # Это поле для пользовательских ролей и прав доступа
        verbose_name='Роль',
        default='user',         # Установил по умолчанию роль "user"
        max_length=30,  
        blank=True
    )


class Category(models.Model):
    name = models.CharField(
        verbose_name='Название категории',
        max_length=256,
        unique=True,
        blank=False
    )
    slug = models.SlugField(
        verbose_name='Slug категории',
        max_length=50,
        unique=True,
        blank=False
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self) -> str:
        return self.name


class Genre(models.Model):
    name = models.CharField(
        verbose_name='Название жанра',
        max_length=256,
        unique=True,
        blank=False
    )
    slug = models.SlugField(
        verbose_name='Slug жанра',
        max_length=50,
        unique=True,
        blank=False
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self) -> str:
        return self.name


class Title(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=256,
        blank=False
    )
    year = models.IntegerField(
        verbose_name='Год выпуска',
        blank=False
    )
    description = models.TextField(
        verbose_name='Описание',
        blank=True,
        null=True
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='genre_title',
        verbose_name='Жанр',
        blank=False
    )
    category = models.ForeignKey(
        Category,
        related_name='category_title',
        verbose_name='Категория',
        on_delete=models.SET_NULL,
        blank=False,
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
        verbose_name='Текст отзыва',
        blank=False
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='review_author',
        verbose_name='Aвтор отзыва'
    )
    score = models.IntegerField(
        verbose_name='Оценка',          # Ограничить оценку в пределах [1 ... 10]
        blank=False
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
        max_length=400,
        blank=False
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