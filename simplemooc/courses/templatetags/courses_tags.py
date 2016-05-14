from django.template import Library

register = Library()

from simplemooc.courses.models import Enrollment

#Carrega um conteudo de uma tag
# no template usar
# {% my_courses %}
# {% <nome-tag> %}
@register.inclusion_tag('courses/templatetags/my_courses.html')
def my_courses(user):
    enrollments = Enrollment.objects.filter(user=user)
    context = {
        'enrollments': enrollments
    }
    return context

#Atualiza o contexto da variavel
# no template usar
# {% load_my_courses user as enrollments %}
# {% load_my_courses <parametros> as <variavel-alterada-no-contexto> %}
@register.assignment_tag
def load_my_courses(user):
    return Enrollment.objects.filter(user=user)