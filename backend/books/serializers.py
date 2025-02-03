from django.contrib.auth.models import Group, User
from .models import Book, Author
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ["url", "username", "email", "groups"]


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ["url", "name"]


class BookSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Book
        fields = ["title", "author", "isbn", "publication_date", "pages"]


class AuthorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Author
        fields = ["first_name", "last_name"]
