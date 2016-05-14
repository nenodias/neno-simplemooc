from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm
from django.contrib.auth.decorators import login_required
from django.conf import settings

from simplemooc.courses.models import Enrollment

from .forms import RegisterForm, EditAccountForm, PasswordResetForm
from .models import PasswordReset

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
            if user:
                login(request, user)
                return redirect(settings.LOGIN_REDIRECT_URL)
            return redirect(settings.LOGIN_URL)
    else:
        form = RegisterForm()
    context = {
        'form': form
    }
    return render(request, template_name, context)

def password_reset(request):
    template_name = 'accounts/password_reset.html'
    form = PasswordResetForm(request.POST or None)
    context = {}
    if form.is_valid():
        form.set_request(request)
        form.save()
        messages.success(request, 'Um e-mail foi enviado para você com mais detalhes')
        return redirect('core:home')
    context['form'] = form
    return render(request, template_name, context)

def password_reset_confirm(request, key):
    template_name = 'accounts/password_reset_confirm.html'
    context = {}
    reset = get_object_or_404(PasswordReset, key=key)
    form = SetPasswordForm(user=reset.user, data=request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'A sua senha foi criada com sucesso')
        return redirect('core:home')
    context['form'] = form
    return render(request, template_name, context)

@login_required
def edit(request):
    template_name = 'accounts/edit.html'
    form = EditAccountForm(request.POST or None, instance=request.user)
    context = {}
    if form.is_valid():
        form.save()
        messages.success(request, 'Os dados foram alterados com sucesso')
        return redirect('accounts:dashboard')
    context['form'] = form
    return render(request, template_name, context)

@login_required
def edit_password(request):
    template_name = 'accounts/edit_password.html'
    form = PasswordChangeForm(data=request.POST or None, user=request.user)
    context = {}
    if form.is_valid():
        form.save()
        messages.success(request, 'A sua senha foi alterada com sucesso')
        return redirect('accounts:dashboard')
    context['form'] = form
    return render(request, template_name, context)