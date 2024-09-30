from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from book.models import Book


# Create your views here.

@login_required()
def course_chat_room(request, book_id):
    try:
        book = Book.objects.last()
    except:
        return HttpResponseForbidden()

    return render(request, 'chat/room.html', context={'book': book})
