from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import MyUserCreationForm


# Create your views here.


def register(request):
    if request.method == 'POST':
        user_form = MyUserCreationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(
                user_form.cleaned_data['password1']
            )
            new_user.save()
            return render(
                request,
                '../templates/account/register_done.html',
                {'new_user': new_user}
            )
    else:
        user_form = MyUserCreationForm()
    return render(
        request,
        '../templates/account/register.html',
        {'user_form': user_form}
    )
