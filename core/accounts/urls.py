from django.urls import path
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from .views import SignUpView, AccountActivationView, LoginView, LogoutView, CustomPasswordResetView, \
    CustomPasswordResetDoneView, CustomPasswordResetConfirmView, CustomPasswordChangeView, ChangePictureView, \
    UserDashboard

app_name = 'accounts'

urlpatterns = [
    path('sign-up/', SignUpView.as_view(), name='sign_up'),
    path('activate/<uidb64>/<token>', AccountActivationView.as_view(), name='account_activation'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('dashboard/', UserDashboard.as_view(), name='dashboard'),

    path('forget-password/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('forget-password/done/', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('forget-password/confirm/<uidb64>/<token>', CustomPasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    # path('forget-password/complete', ),
    path('password-change/', CustomPasswordChangeView.as_view(), name='password_change'),
    path('password-change/done/', PasswordChangeDoneView.as_view(), name='password_change_done'),
    # path('dashboard/', UserProfileView.as_view(), name='dahsboard')
    path('change-profile/', ChangePictureView.as_view(), name='profile_picture_change')
]
