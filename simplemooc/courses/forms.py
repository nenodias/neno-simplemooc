from django import forms
from django.core.mail import send_mail
from django.conf import settings

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
        messsge = 'Nome: %(name)s;E-Mail: %(email)s;%(messsge)s'
        context ={
            'name':self.cleaned_data['name']
            'email':self.cleaned_data['email']
            'message':self.cleaned_data['message']
        }
        message = message %(context)
        send_mail(
            subject, 
            message, 
            settings.DEFAULT_FROM_EMAIL,
            [settings.CONTACT_EMAIL]
        )