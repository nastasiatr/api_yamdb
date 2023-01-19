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
    'users',
    UsersViewSet,
    basename='users'
)
router.register(
    'categories',
    CategoryViewSet,
    basename='сategories'
)
router.register(
    'genres',
    GenreViewSet,
    basename='genres'
)
router.register(
    'titles',
    TitleViewSet,
    basename='titles'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

urlpatterns = [
    path('v1/', include(router.urls)),
    # Здесь будет что-то с регистрацией и токенами
]