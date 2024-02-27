from django.contrib import admin
from .models import Book, Author, BookAuthor, BookReview


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'isbn', 'description')
    search_fields = ('title', 'isbn')


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'biography')


@admin.register(BookAuthor)
class BookAuthorAdmin(admin.ModelAdmin):
    list_display = ('book', 'author')


@admin.register(BookReview)
class BookReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'comment', 'stars_given')
