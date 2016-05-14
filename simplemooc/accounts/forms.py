from django import forms
from django.contrib.auth import get_user_model

from simplemooc.core.utils import generate_hash_key
from simplemooc.core.mail import send_mail_template

User = get_user_model()

from .models import PasswordReset

class PasswordResetForm(forms.Form):

    email = forms.EmailField(label='E-mail')

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            return email
        else:
            raise forms.ValidationError('Nenhum usuário encontrado com este E-mail')

    def save(self):
        user = User.objects.get( email=self.cleaned_data['email'] )
        key = generate_hash_key(user.username)
        reset = PasswordReset(user=user, key=key)
        reset.save()
        template_name = 'accounts/password_reset_mail.html'
        domain = self.request.build_absolute_uri('/')[:-1]
        subject = 'Criar nova senha no SimpleMooc'
        context = {
            'reset': reset,
            'domain': domain
        }
        send_mail_template(subject, template_name, context, [ user.email ])

    def set_request(self, req):
        self.request = req

class RegisterForm(forms.ModelForm):

    email = forms.EmailField(label='E-mail')
    password1 = forms.CharField(label='Senha', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmação de Senha', widget=forms.PasswordInput)

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.set_password( self.cleaned_data['password1'] )
        if commit:
            user.save()
        return user

    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('A confirmação de senha está incorreta')
        return password2

    class Meta:
        model = User
        fields = ['username', 'email']


class EditAccountForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'email', 'name']
