from django.urls import path
from .views import SignUpView, AccountActivationView, LoginView, LogoutView

app_name = 'accounts'

urlpatterns = [
    path('sign-up/', SignUpView.as_view(), name='sign_up'),
    path('activate/<uidb64>/<token>', AccountActivationView.as_view(), name='account_activation'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
