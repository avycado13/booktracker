from django.contrib import admin

from .models import Media, Author, Review, Shelf, List

admin.site.register(Media)
admin.site.register(Author)
admin.site.register(Review)
admin.site.register(Shelf)
admin.site.register(List)
