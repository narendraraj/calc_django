import email
from turtle import Turtle
from django.shortcuts import render, redirect
from django.http import HttpResponse, request, Http404
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView

from django.contrib.auth import login, authenticate
from account.forms import CustomUserCreationForm

from django.views.generic.edit import CreateView, FormView
from django.contrib.auth import get_user_model

# Create your views here.
MyUser = get_user_model()


class CustomLoginView(LoginView):

    template_name = 'account/account_login.html'
    fields = '__all__'
    redirect_authenticated_user = True
    # success_url = reverse_lazy('account:account_home')

    def get_success_url(self):
        return reverse_lazy('account:account_home')


class CustomRegisterView(CreateView):
    template_name = "account/account_register.html"
    form_class = CustomUserCreationForm    
    redirect_authenticated_user = True
    success_url = reverse_lazy("d_spacing:database_list")
    

# def account_register(request):

#     if request.user.is_authenticated:
#         return redirect('account:account_home')

#     if request.method == 'POST':
#         register_form = CustomUserCreationForm(request.POST)
#         if register_form.is_valid():
#             user = register_form.save(commit=False)
#             user.email = register_form.cleaned_data['email']
#             user.set_password(register_form.cleaned_data['password'])
#             user.is_active = True
#             user.save()

#             # current_site = get_current_site(request)
#             # subject = 'Activate your Account'
#             # message = render_to_string('account/registration/account_activation_email.html', {
#             #     'user': user,
#             #     'domain': current_site.domain,
#             #     'uid': urlsafe_base64_encode(force_bytes(user.pk)),
#             #     'token': account_activation_token.make_token(user),
#             # })
#             # user.email_user(subject=subject, message=message)
#             # return HttpResponse('registered succesfully and activation sent')
#     else:
#         register_form = CustomUserCreationForm()

#     return render(request, 'account/account_register.html', {'form': register_form})


def account_home_view(request):

    accounts = MyUser.objects.all()

    context = {
        "accounts": accounts

    }

    return render(request, "account/account_home.html", context)
