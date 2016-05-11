from django.shortcuts import render, get_object_or_404

from .models import Course
from .forms import ContactCourse

def index(request):
    courses = Course.objects.all()
    template_name = 'courses/index.html'
    context = {
        'courses':courses
    }
    return render(request, template_name, context)

def details(request, slug):
    course = get_object_or_404(Course,slug=slug)
    template_name = 'courses/details.html'
    context = {}
    if request.method == 'POST':
        form = ContactCourse(request.POST)
        if form.is_valid():
            form.send_mail()
            form = ContactCourse()
            context['is_valid'] = True
    else:
        form = ContactCourse()
    context['course'] = course
    context['form'] = form
    return render(request, template_name, context)