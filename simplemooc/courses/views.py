from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Course, Enrollment, Announcement
from .forms import ContactCourse, CommentForm

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
            form.send_mail(course)
            form = ContactCourse()
            context['is_valid'] = True
    else:
        form = ContactCourse()
    context['course'] = course
    context['form'] = form
    return render(request, template_name, context)

@login_required
def enrollment(request, slug):
    course = get_object_or_404(Course, slug=slug)
    enrollment, created = Enrollment.objects.get_or_create(
        user=request.user, course=course
    )
    if created:
        messages.success(request, 'Você foi inscrito no curso com sucesso')
    else:
        messages.info(request, 'Você já está inscrito no curso')
    return redirect('accounts:dashboard')

@login_required
def undo_enrollment(request, slug):
    course = get_object_or_404(Course,slug=slug)
    enrollment = get_object_or_404(Enrollment, user=request.user, course=course)
    template_name = 'courses/undo_enrollment.html'
    if request.POST:
        enrollment.delete()
        messages.success(request, 'Sua inscrição no curso {0} foi cancelada'.format(course) )
        return redirect('accounts:dashboard')
    context = {
        'course':course,
        'enrollment':enrollment
    }
    return render(request, template_name, context)

@login_required
def announcements(request, slug):
    course = get_object_or_404(Course,slug=slug)
    enrollment = get_object_or_404(Enrollment, user=request.user, course=course)
    if not request.user.is_staff:
        if not enrollment.is_approved():
            messages.error(request, 'Sua inscrição está pendente')
            return redirect('accounts:dashboard')
    template_name = 'courses/announcements.html'
    context = {
        'course':course,
        'announcements': course.announcements.all()
    }
    return render(request, template_name, context)

@login_required
def show_announcement(request, slug, pk):
    course = get_object_or_404(Course,slug=slug)
    enrollment = get_object_or_404(Enrollment, user=request.user, course=course)
    if not request.user.is_staff:
        if not enrollment.is_approved():
            messages.error(request, 'Sua inscrição está pendente')
            return redirect('accounts:dashboard')
    announcement = get_object_or_404(course.announcements.all(), pk=pk)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.announcement = announcement
        comment.user = request.user
        comment.save()
        form = CommentForm()
        messages.success(request, 'Seu comentário foi enviado com sucesso')
    template_name = 'courses/show_announcement.html'
    context = {
        'course':course,
        'announcement': announcement,
        'form':form
    }
    return render(request, template_name, context)