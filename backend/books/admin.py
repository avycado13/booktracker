from django.contrib import admin

from .models import Book, Author, Review, Shelf, List

admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Review)
admin.site.register(Shelf)
admin.site.register(List)