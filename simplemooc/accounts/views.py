from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.conf import settings

from .forms import RegisterForm

def register(request):
    template_name = 'accounts/register.html'
    if request.POST:
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user = authenticate(
                username=user.username, password=form.cleaned_data['password1'] 
            )
            return redirect(settings.LOGIN_URL)
    else:
        form = RegisterForm()
    context = {
        'form': form
    }
    return render(request, template_name, context)

def logout(request):
    pass