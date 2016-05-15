from django.db import models
from django.conf import settings

from simplemooc.core.mail import send_mail_template

class CourseManager(models.Manager):
    
    def search(self, query):
        '''
        Consulta filtrando com OU utiliza o models.Q com o | (pipe)
        '''
        return self.get_queryset().filter(
            models.Q(name__icontains=query)|
            models.Q(description__icontains=query)
        )

class Course(models.Model):

    objects = CourseManager()

    name = models.CharField('Nome', max_length=100)
    slug = models.SlugField('Atalho')
    description = models.TextField('Descrição Simples', blank=True)
    about = models.TextField('Sobre o Curso')
    start_date = models.DateField('Data de Início', null=True, blank=True)
    imagem = models.ImageField(
        upload_to='courses/images',
        verbose_name='Imagem',
        null=True, blank=True
    )
    create_at = models.DateTimeField('Criado em', auto_now_add=True)
    update_at = models.DateTimeField('Atualizado em', auto_now=True)

    def __str__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        #from django.core.urlresolvers import reverse
        return ('courses:details',(), { 'slug' : self.slug } )

    class Meta:
        verbose_name = 'Curso'
        verbose_name_plural = 'Cursos'
        ordering = ['name']

class Enrollment(models.Model):

    STATUS_CHOICES = (
        (0,'Pendente'),
        (1,'Aprovado'),
        (2,'Cancelado'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Usuário',
        related_name='enrollments'
    )
    course = models.ForeignKey(Course, verbose_name='Curso',
        related_name='enrollments'
    )
    status = models.IntegerField('Situação', choices=STATUS_CHOICES, default=1, blank=True)
    create_at = models.DateTimeField('Criado em', auto_now_add=True)
    update_at = models.DateTimeField('Atualizado em', auto_now=True)

    def is_approved(self):
        return status == 1

    class Meta:
        verbose_name = 'Inscrição'
        verbose_name_plural = 'Inscrições'
        unique_together = ( ('user', 'course'), )

class Announcement(models.Model):

    course = models.ForeignKey(Course, verbose_name='Curso', related_name='announcements')
    title = models.CharField('Título', max_length = 100)
    content = models.TextField('Conteúdo')
    
    create_at = models.DateTimeField('Criado em', auto_now_add=True)
    update_at = models.DateTimeField('Atualizado em', auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Anúncio'
        verbose_name_plural = 'Anúncios'
        ordering = ['-create_at']

class Comment(models.Model):

    announcement = models.ForeignKey(Announcement,
        verbose_name='Anúncio',
        related_name='comments'
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Usuário',
        related_name='comments'
    )
    comment = models.TextField('Comentário')
    create_at = models.DateTimeField('Criado em', auto_now_add=True)
    update_at = models.DateTimeField('Atualizado em', auto_now=True)

    class Meta:
        verbose_name = 'Comentário'
        verbose_name_plural = 'Comentários'
        ordering = ['create_at']

def post_save_announcement(instance, created, **kwargs):
    subject = instance.title
    context = {
        'announcement':instance
    }
    template_name = 'courses/announcement_mail.html'
    enrollments = Enrollment.objects.filter(course=instance.course,status=1)
    for enrollment in enrollments:
        recipient_list = [enrollment.user.email]
        send_mail_template(subject, template_name, context, recipient_list)

models.signals.post_save.connect(
    post_save_announcement,
    sender=Announcement,
    dispatch_uid='post_save_announcement'
)