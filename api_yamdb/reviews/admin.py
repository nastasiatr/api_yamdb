from django.contrib import admin

from reviews.models import User, Category, Genre, Title, Review, Comment


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'bio',
        'role'
    )
    search_fields = ('username',)
    list_filter = ('username',)
    empty_value_display = '-пусто-'


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'slug'
    )
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'


class GenreAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'slug'
    )
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'


class TitleAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'year',
        'description',
        'genre',
        'category'
    )
    search_fields = (        
        'name',
        'year',
        'genre',
        'category'
    )
    list_filter = (
        'name',
        'year',
        'genre',
        'category'
    )
    empty_value_display = '-пусто-'


class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'text',
        'author',
        'score',
        'pub_date'
    )
    search_fields = ('author', 'pub_date',)
    list_filter = ('pub_date', 'score',)
    empty_value_display = '-пусто-'


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'review',
        'text',
        'author',
        'pub_date'
    )
    search_fields = ('review', 'author',)
    list_filter = ('review', 'pub_date',)
    empty_value_display = '-пусто-'


admin.site.register(User, UserAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)