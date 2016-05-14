from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.conf import settings

from .forms import RegisterForm, EditAccountForm

@login_required
def dashboard(request):
    template_name = 'accounts/dashboard.html'
    return render(request, template_name)

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

@login_required
def edit(request):
    template_name = 'accounts/edit.html'
    form = EditAccountForm(request.POST or None, instance=request.user)
    context = {}
    if form.is_valid():
        form.save()
        context['success'] = True
    context['form'] = form
    return render(request, template_name, context)

@login_required
def edit_password(request):
    template_name = 'accounts/edit_password.html'
    context = {}
    return render(request, template_name, context)