from django.db import models
from django.utils import timezone
# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey('Author', on_delete=models.CASCADE, related_name='books')
    publication_date = models.DateField()
    isbn = models.CharField(max_length=13)
    pages = models.IntegerField()
    cover_image = models.ImageField(upload_to="covers/", blank=True)
    summary = models.TextField(blank=True)
    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return f"/books/{self.id}/"
    def published_in_last(self, months=12):
        return self.publication_date.month >= timezone.now().month - months
    
class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    bio = models.TextField(blank=True)
    def __str__(self):
        return f"{self.first_name} {self.last_name}"