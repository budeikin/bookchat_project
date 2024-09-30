from django.urls import path
from .views import HomePageTemplateView

app_name = 'home'

urlpatterns = [
    path('', HomePageTemplateView.as_view(), name='home_page'),
    # path('<slug:category_slug>/', HomePageTemplateView.as_view(), name='books_by_category'),
]
