from django.db import models
from taggit.managers import TaggableManager
from django.conf import settings

class Thread(models.Model):
    
    title = models.CharField('Título', max_length=100)
    body = models.TextField('Mensagem')
    views = models.IntegerField('Visualizações', blank=True, default=0)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Autor',
        related_name='threads'
    )
    answers = models.IntegerField('Respostas', blank=True, default=0)
    tags = TaggableManager()

    create_at = models.DateTimeField('Criado em', auto_now_add=True)
    update_at = models.DateTimeField('Modificado em', auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Tópico'
        verbose_name_plural = 'Tópicos'
        ordering = ['-update_at']

class Reply(models.Model):

    reply = models.TextField('Resposta')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Autor',
        related_name='replies'
    )
    thread = models.ForeignKey(Thread, verbose_name='Tópico',
        related_name='replies'
    )
    correct = models.BooleanField('Correta', blank=True, default=False)

    create_at = models.DateTimeField('Criado em', auto_now_add=True)
    update_at = models.DateTimeField('Modificado em', auto_now=True)

    def __str__(self):
        return self.reply[:100]

    class Meta:
        verbose_name = 'Resposta'
        verbose_name_plural = 'Respostas'
        ordering = ['-correct', 'create_at']

def post_save_reply(created, instance, **kwargs):
    instance.thread.answers = instance.thread.replies.count()
    instance.thread.save()

def post_delete_reply(created, instance, **kwargs):
    instance.thread.answers = instance.thread.replies.count()
    instance.thread.save()

models.signals.post_save.connect(
    post_save_reply, sender=Reply, dispatch_uid='post_save_reply'
)
models.signals.post_delete.connect(
    post_delete_reply, sender=Reply, dispatch_uid='post_delete_reply'
)