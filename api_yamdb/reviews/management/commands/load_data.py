from csv import DictReader
from django.core.management import BaseCommand
from django.db.models import Avg

from users.models import User
from reviews.models import (Category,
                            Comment,
                            Genre,
                            GenreTitle,
                            Review,
                            Title)


class Command(BaseCommand):
    def making_import(self, *args, **options):
        if (Genre.objects.exists()
                or User.objects.exists()
                or Comment.objects.exists()
                or Review.objects.exists()
                or Title.objects.exists()
                or Category.objects.exists()
                or GenreTitle.objects.exists()):
            print('Перед запуском импорта, очистите базу данных.'
                  'Используйте команду "python manage.py flush"')
            exit()
        print("Процесс импорта данных запущен")

        for row in DictReader(open('static/data/users.csv',
                                   encoding='utf-8')):
            try:
                user = User(id=row['id'],
                            username=row['username'],
                            email=row['email'],
                            role=row['role'],
                            bio=row['bio'],
                            irst_name=row['first_name'],
                            last_name=row['last_name'])
                user.save()
            except Exception as e:
                print(f'Сбой!'
                      f'Ошибка импорта "User" в строчке {row} - {e}')
        print('Импорт "User" завершен успешно!')

        for row in DictReader(open('static/data/genre.csv',
                                   encoding='utf-8')):
            try:
                genre = Genre(id=row['id'],
                              name=row['name'],
                              slug=row['slug'])
                genre.save()
            except Exception as e:
                print(f'Сбой!'
                      f'Ошибка импорта "Genre" в строчке {row} - {e}')
        print("Импорт Genre завершен успешно")

        for row in DictReader(open('static/data/category.csv',
                                   encoding='utf-8')):
            try:
                category = Category(id=row['id'],
                                    name=row['name'],
                                    slug=row['slug'])
                category.save()
            except Exception as e:
                print(f'Сбой!'
                      f'Ошибка импорта "Category" в строчке {row} - {e}')
        print('Импорт "Category" завершен успешно')

        for row in DictReader(open('static/data/titles.csv',
                                   encoding='utf-8')):
            try:
                category = Category.objects.get(id=row['category'])
                title = Title(id=row['id'],
                              name=row['name'],
                              year=row['year'],
                              category=category)
                title.save()
            except Exception as e:
                print(f'Сбой!'
                      f'Ошибка импорта "Title" в строчке {row} - {e}')
        print('Импорт "Title" завершен успешно')

        for row in DictReader(open('static/data/genre_title.csv',
                                   encoding='utf-8')):
            try:
                genre = Genre.objects.get(id=row['genre_id'])
                title = Title.objects.get(id=row['title_id'])
                genre_title = GenreTitle(id=row['id'],
                                         title=title,
                                         genre=genre)
                genre_title.save()
            except Exception as e:
                print(f'Сбой!'
                      f'Ошибка импорта "GenreTitle" в строчке {row} - {e}')
        print('Импорт "GenreTitle" завершен успешно')

        for row in DictReader(open('static/data/review.csv',
                                   encoding='utf-8')):
            try:
                title = Title.objects.get(id=row['title_id'])
                author = User.objects.get(id=row['author'])
                review = Review(id=row['id'],
                                title=title,
                                text=row['text'],
                                author=author,
                                score=row['score'],
                                pub_date=row['pub_date'])
                review.save()
                avg_title = title.reviews.aggregate(Avg('score'))
                title.rating = int(avg_title['score__avg'])
                title.save()
            except Exception as e:
                print(f'Сбой!'
                      f'Ошибка импорта "Review" в строчке {row} - {e}')
        print('Импорт "Review" завершен успешно')

        for row in DictReader(open('static/data/comments.csv',
                                   encoding='utf-8')):
            try:
                review = Review.objects.get(id=row['review_id'])
                author = User.objects.get(id=row['author'])
                comment = Comment(id=row['id'],
                                  review=review,
                                  text=row['text'],
                                  author=author,
                                  pub_date=row['pub_date'])
                comment.save()
            except Exception as e:
                print(f'Сбой!'
                      f'Ошибка импорта "Comment" в строчке {row} - {e}')
        print('Импорт "Comment" завершен успешно')
