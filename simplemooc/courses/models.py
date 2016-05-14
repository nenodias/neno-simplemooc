from django.db import models
from django.conf import settings


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

    class Meta:
        verbose_name = 'Inscrição'
        verbose_name_plural = 'Inscrições'
        unique_together = ( ('user', 'course'), )