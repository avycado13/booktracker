from django.urls import path

from . import views


app_name = "books"


urlpatterns = [
    path("", views.index, name="index"),
    path('accounts/login/', views.login_page, name='login_page'),    # Login page
    path('accounts/register/', views.register_page, name='register'),  # Registration page
    path("book/<int:book_id>/", views.book_detail, name="book_detail"),
    path("author/<int:author_id>/", views.author_detail, name="author_detail"),
    path("add_to_shelf/<int:book_id>/<int:shelf_id>/", views.add_to_shelf, name="add_to_shelf"),
    path("mark_as_read/<int:book_id>/", views.mark_as_read, name="mark_as_read"),
]
