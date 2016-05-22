from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Course, Enrollment, Announcement, Lesson, Material
from .forms import ContactCourse, CommentForm
from .decorators import enrolment_required

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
    course = request.course
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
    course = request.course
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
@enrolment_required
def announcements(request, slug):
    course = request.course
    template_name = 'courses/announcements.html'
    context = {
        'course':course,
        'announcements': course.announcements.all()
    }
    return render(request, template_name, context)

@login_required
@enrolment_required
def show_announcement(request, slug, pk):
    course = request.course
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

@login_required
@enrolment_required
def lessons(request, slug):
    course = request.course
    lessons = course.release_lessons()
    if request.user.is_staff:
        lessons = course.lessons.all()
    template_name = 'courses/lessons.html'
    context = {
        'course':course,
        'lessons':lessons
    }
    return render(request, template_name, context)

@login_required
@enrolment_required
def lesson(request, slug, pk):
    course = request.course
    lesson = get_object_or_404(course.release_lessons(), pk=pk)
    if not request.user.is_staff or not lesson.is_avaliable():
        messages.error(request, 'Esta aula não está disponível')
        return redirect('courses:lessons', slug=course.slug)
    template_name = 'courses/lesson.html'
    context = {
        'course':course,
        'lesson':lesson
    }
    return render(request, template_name, context)

@login_required
@enrolment_required
def material(request, slug, pk):
    course = request.course
    material = get_object_or_404(Material, pk=pk, lesson__course=course)
    lesson = material.lesson
    if not request.user.is_staff and not lesson.is_avaliable():
        messages.error(request, 'Esta aula não está disponível')
        return redirect('courses:lessons', slug=course.slug)
    if not material.is_embedded() and material.file:
        return redirect(material.file.url)
    template_name = 'courses/material.html'
    context = {
        'course':course,
        'lesson':lesson,
        'material':material
    }
    return render(request, template_name, context)
    return render