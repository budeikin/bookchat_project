from django.urls import path
from .views import SignUpView, AccountActivationView

#
urlpatterns = [
    path('sign-up/', SignUpView.as_view(), name='sign_up'),
    path('activate/<uidb64>/<token>', AccountActivationView.as_view(), name='account_activation')
]
