from django.urls import path

from . import views
app_name = 'books'


urlpatterns = [
    path("", views.index, name="index"),
    path("book/<int:book_id>/", views.book_detail, name="detail")
]