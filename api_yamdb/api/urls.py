from django.urls import include, path

from rest_framework.routers import DefaultRouter

from api.views import (UsersViewSet,
                       CategoryViewSet,
                       GenreViewSet,
                       TitleViewSet,
                       ReviewViewSet,
                       CommentViewSet)


router = DefaultRouter()

router.register(
    # Здесь будет эндпоинт пользователей
    UsersViewSet,
    basename='users'
)
router.register(
    # Здесь будет эндпоинт категорий
    CategoryViewSet,
    basename='сategories'
)
router.register(
    # Здесь будет эндпоинт жанров
    GenreViewSet,
    basename='genres'
)
router.register(
    # Здесь будет эндпоинт произведений
    TitleViewSet,
    basename='titles'
)
router.register(
    # Здесь будет эндпоинт отзывов
    ReviewViewSet,
    basename='reviews'
)
router.register(
    # Здесь будет эндпоинт комментов
    CommentViewSet,
    basename='comments'
)

urlpatterns = [
    path('v1/', include(router.urls)),
    # Здесь будет что-то с регистрацией и токенами
]