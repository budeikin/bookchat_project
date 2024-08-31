from django.shortcuts import render
from django.views.generic import TemplateView
from book.models import Author, Book


# Create your views here.

class HomePageTemplateView(TemplateView):
    template_name = 'home/home_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['last_book'] = Book.objects.last()
        return context
