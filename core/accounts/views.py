from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.views.generic import View
from django.core.mail import EmailMessage
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .forms import SignUpForm
from .models import CustomUser
from .tokens import account_activation_token


# Create your views here.

class SignUpView(View):
    def get(self, request, *args, **kwargs):
        signup_form = SignUpForm()
        return render(request, 'accounts/signup.html', context={'signup_form': signup_form})

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
                return HttpResponse('and email send to you , click on the link on it')
        return render(request, 'accounts/signup.html', context={'signup_form': signup_form})


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
            return HttpResponse('your account is active now')
        else:
            raise HttpResponse('something went wrong')
