from django.contrib.auth.forms import SetPasswordForm
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes, force_str
from django.views.generic import View, TemplateView
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView, PasswordResetDoneView, \
    PasswordResetCompleteView, PasswordChangeView
from django.core.mail import EmailMessage
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth import login, logout
from .forms import SignUpForm, LoginForm, ProfilePictureChangeForm
from .models import CustomUser
from .tokens import account_activation_token


# Create your views here.

# sign up view
class SignUpView(View):
    def get(self, request, *args, **kwargs):
        signup_form = SignUpForm()
        return render(request, 'accounts/registration/signup.html', context={'signup_form': signup_form})

    def post(self, request, *args, **kwargs):
        signup_form = SignUpForm(request.POST)
        if signup_form.is_valid():
            user_email = signup_form.cleaned_data.get('email')
            if CustomUser.objects.filter(email__iexact=user_email).exists():
                signup_form.add_error('email', 'this email address already exists')
            else:
                user = signup_form.save(commit=False)
                user.is_active = False
                user.save()
                current_site = get_current_site(request)
                mail_subject = 'Account Activation'
                message = render_to_string('accounts/emails/activate_account.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user)
                })
                email = EmailMessage(mail_subject, message, to=['user_email'])
                email.send()

                messages.success(request, 'an activation code sent to your email check it')
                return HttpResponse('and email send to you , click on the link on it')
        return render(request, 'accounts/registration/signup.html', context={'signup_form': signup_form})


# account activation view
class AccountActivationView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(pk=uid)

        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()

            messages.success(request, 'your account is active now')
            return redirect('accounts:login')
        else:
            raise HttpResponse('something went wrong')


# log in  view
class LoginView(View):
    def get(self, request, *args, **kwargs):
        login_form = LoginForm()
        return render(request, 'accounts/registration/login.html', context={'login_form': login_form})

    def post(self, request, *args, **kwargs):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_email = login_form.cleaned_data['email']
            user_password = login_form.cleaned_data['password']
            user = CustomUser.objects.filter(email__iexact=user_email).first()
            if user:
                if user.is_active:
                    is_currect_password = user.check_password(user_password)
                    if is_currect_password:
                        login(request, user)

                        messages.success(request, 'you logged in successfully')
                        return redirect('home:home_page')
                    else:
                        login_form.add_error('password', 'something went wrong')
                else:
                    login_form.add_error('email', 'your account is not active')
            else:
                login_form.add_error('email', "this user does not exist")

            return render(request, 'accounts/registration/login.html', context={'login_form': login_form})

        return redirect('accounts:login')


# log out view
class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        messages.success(request, 'you logged out successfully')
        return redirect('home:home_page')


# forgot password views
class CustomPasswordResetView(PasswordResetView):
    email_template_name = 'accounts/emails/password_reset_email.html'
    template_name = 'accounts/registration/password_reset.html'
    success_url = reverse_lazy('accounts:password_reset_done')


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'accounts/registration/password_reset_done.html'


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'accounts/registration/password_reset_confirm.html'
    # form_class = SetPasswordForm
    # token_generator = account_activation_token
    success_url = reverse_lazy('home:home_page')


class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'accounts/registration/password_change_form.html'
    success_url = reverse_lazy('home:home_page')
    success_message = 'your password changed successfully'

    def form_valid(self, form):
        response = super().form_valid(form)
        success_message = self.get_success_message(form.cleaned_data)
        if success_message:
            messages.success(self.request, success_message)
        return response

    def get_success_message(self, cleaned_data):
        return self.success_message % cleaned_data


class ChangePictureView(View):

    def get(self, request):
        form = ProfilePictureChangeForm(instance=request.user)
        return render(request, 'accounts/registration/profile_picture_change.html', context={'form': form})

    def post(self, request):
        form = ProfilePictureChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save(commit=True)
            messages.success(request, 'profile changed successfully')
        return render(request, 'accounts/registration/profile_picture_change.html', context={'form': form})


class UserDashboard(TemplateView):
    template_name = 'accounts/user_panel/dashboard.html'
