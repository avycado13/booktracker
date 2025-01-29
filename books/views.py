from django.shortcuts import render,get_object_or_404
from .models import Book,Author


# Create your views here.
def index(request):
    books = Book.objects.all()
    context = {'books': books}
    return render(request, 'books/index.html', context)

def book_detail(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    context = {'book': book}
    return render(request, 'books/book_detail.html', context)


def author_detail(request, author_id):
    author = get_object_or_404(Author, pk=author_id)
    context = {'author': author}
    return render(request, 'books/book_detail.html', context)