from django.shortcuts import render
from django.views.generic import TemplateView, View, ListView

from .models import Thread, Reply

class ForumView(ListView):

    model = Thread
    paginate_by = 2
    template_name = 'forum/index.html'

    def get_context_data(self, **kwargs):
        context = super(ForumView, self).get_context_data(**kwargs)
        context['tags'] = Thread.tags.all()
        return context

index = ForumView.as_view()