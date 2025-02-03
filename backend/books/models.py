from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator


class Author(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Author, related_name="books", on_delete=models.CASCADE)
    publication_date = models.DateField()
    isbn = models.CharField(max_length=13, unique=True)
    pages = models.IntegerField()
    cover_image = models.ImageField(upload_to="covers/", blank=True)
    summary = models.TextField(blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f"/books/{self.id}/"

    def published_in_last(self, months=12):
        from dateutil.relativedelta import relativedelta
        return self.publication_date >= timezone.now().date() - relativedelta(months=months)

    def is_read_by(self, user):
        read_books_list = List.objects.filter(user=user, name="Read Books").first()
        if not read_books_list:
            read_books_list = List.objects.create(user=user, name="Read Books")
        if read_books_list:
            return self in read_books_list.books.all()
        return False
    def mark_as_read(self, user):
        read_books_list = List.objects.filter(user=user, name="Read Books").first()
        to_be_read_list = List.objects.filter(user=user, name="To Be Read").first()
        if not read_books_list:
            read_books_list = List.objects.create(user=user, name="Read Books")
        if not to_be_read_list:
            to_be_read_list = List.objects.create(user=user, name="To Be Read")
        read_books_list.books.add(self)
        if self in to_be_read_list.books.all():
            to_be_read_list.books.remove(self)
        return True


class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="reviews")
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.rating} - {self.book.title}"


class Shelf(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="shelves")
    books = models.ManyToManyField(Book, related_name="shelves")  # Fixed redundant definition

    def __str__(self):
        return f"{self.name} ({self.user.username})"


class List(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="lists")
    books = models.ManyToManyField(Book, related_name="lists")  # Fixed redundant definition

    def __str__(self):
        return f"{self.name} ({self.user.username})"
