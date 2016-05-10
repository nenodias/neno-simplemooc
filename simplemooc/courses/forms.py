from django import forms

class ContactCourse(forms.Form):

    name = forms.CharField(label='Nome', max_length=100, required=True)
    email = forms.EmailField(label='Email', required=True)
    mensagem = forms.CharField(
        label='Mensagem/Dúvida',
        widget=forms.Textarea,
        required=True
        )