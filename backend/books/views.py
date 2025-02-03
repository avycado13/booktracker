from django.shortcuts import render, redirect, get_object_or_404
from .models import Book, Author, Shelf, List
from django.contrib.auth.models import Group, User
from django.contrib import messages
from django.contrib.auth import authenticate, login
from rest_framework import permissions, viewsets
from .serializers import (
    BookSerializer,
    AuthorSerializer,
    UserSerializer,
    GroupSerializer,
)
from django.contrib.auth.decorators import login_required



# Create your views here.
@login_required
def index(request):
    shelves = request.user.shelves.all()
    books = Book.objects.all()
    books_read = [books for book in books if book.is_read_by(request.user)]
    list_read = List.objects.filter(user=request.user, name="Read Books").first()
    context = {"books": books,"shelves":shelves,"user": request.user, "books_read":list_read.books.all()}
    return render(request, "books/index.html", context)


def book_detail(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    context = {"book": book, "author": book.author, "reviews": book.reviews.all(),"user": request.user}
    return render(request, "books/book_detail.html", context)


def author_detail(request, author_id):
    author = get_object_or_404(Author, pk=author_id)
    context = {"author": author, "books": author.books.all(),"user": request.user}
    return render(request, "books/author_detail.html", context)

def add_to_shelf(request, book_id, shelf_id):
    book = get_object_or_404(Book, pk=book_id)
    shelf = get_object_or_404(Shelf, pk=shelf_id)
    shelf.books.add(book)
    return redirect("book_detail", book_id=book_id)

def mark_as_read(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    book.mark_as_read(request.user)
    return redirect("index", book_id=book_id)



# Define a view function for the login page
def login_page(request):
    # Check if the HTTP request method is POST (form submission)
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        # Check if a user with the provided username exists
        if not User.objects.filter(username=username).exists():
            # Display an error message if the username does not exist
            messages.error(request, "Invalid Username")
            return redirect("/login/")

        # Authenticate the user with the provided username and password
        user = authenticate(username=username, password=password)

        if user is None:
            # Display an error message if authentication fails (invalid password)
            messages.error(request, "Invalid Password")
            return redirect("/login/")
        else:
            # Log in the user and redirect to the home page upon successful login
            login(request, user)
            return redirect("/")

    # Render the login page template (GET request)
    return render(request, "books/login.html")


# Define a view function for the registration page
def register_page(request):
    # Check if the HTTP request method is POST (form submission)
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        password = request.POST.get("password")

        # Check if a user with the provided username already exists
        user = User.objects.filter(username=username)

        if user.exists():
            # Display an information message if the username is taken
            messages.info(request, "Username already taken!")
            return redirect("/register/")

        # Create a new User object with the provided information
        user = User.objects.create_user(
            first_name=first_name, last_name=last_name, username=username
        )

        # Set the user's password and save the user object
        user.set_password(password)
        user.save()

        # Display an information message indicating successful account creation
        messages.info(request, "Account created Successfully!")
        return redirect("/login/")

    # Render the registration page template (GET request)
    return render(request, "books/register.html")


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """

    queryset = Group.objects.all().order_by("name")
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class BookViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows books to be viewed or edited.
    """

    queryset = Book.objects.all().order_by("title")
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]


class AuthorViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows authors to be viewed or edited.
    """

    queryset = Author.objects.all().order_by("name")
    serializer_class = AuthorSerializer
    permission_classes = [permissions.IsAuthenticated]
