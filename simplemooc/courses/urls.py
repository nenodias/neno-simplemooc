from django.conf.urls import patterns, include, url

urlpatterns = patterns('simplemooc.courses.views',
    # Regex , Método da view, nome
    url(r'^$', 'index', name='index'),
)
