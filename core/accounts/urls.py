from django.urls import path
from .views import SignUpView, AccountActivationView, LoginView, LogoutView, CustomPasswordResetView, \
    CustomPasswordResetDoneView, CustomPasswordResetConfirmView

app_name = 'accounts'

urlpatterns = [
    path('sign-up/', SignUpView.as_view(), name='sign_up'),
    path('activate/<uidb64>/<token>', AccountActivationView.as_view(), name='account_activation'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('forget-password', CustomPasswordResetView.as_view(), name='password_reset'),
    path('forget-password/done/', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('forget-password/confirm/<uidb64>/<token>', CustomPasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    # path('forget-password/complete', ),
]
