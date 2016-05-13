from django import forms
from django.core.mail import send_mail
from django.conf import settings

from simplemooc.core.mail import send_mail_template

class ContactCourse(forms.Form):

    name = forms.CharField(label='Nome', max_length=100, required=True)
    email = forms.EmailField(label='Email', required=True)
    mensagem = forms.CharField(
        label='Mensagem/Dúvida',
        widget=forms.Textarea,
        required=True
        )

    def send_mail(self, course):
        subject = '[%s] Contato' %(course)
        context ={
            'name':self.cleaned_data['name'],
            'email':self.cleaned_data['email'],
            'message':self.cleaned_data['mensagem']
        }
        template_name = 'courses/contact_email.html'
        send_mail_template(
            subject,
            template_name,
            context,
            [settings.CONTACT_EMAIL]
        )