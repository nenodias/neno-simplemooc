from django.shortcuts import render
from django.views.generic import TemplateView, View, ListView

from .models import Thread, Reply

class ForumView(ListView):

    paginate_by = 2
    template_name = 'forum/index.html'

    def get_queryset(self):
        queryset = Thread.objects.all()
        self.order = self.request.GET.get('order', '')
        if self.order == 'views':
            queryset = queryset.order_by('-views')
        elif self.order == 'answers':
            queryset = queryset.order_by('-answers')
        tag = self.kwargs.get('tag', '')
        if tag:
            queryset = queryset.filter(tags__slug__icontains=tag)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(ForumView, self).get_context_data(**kwargs)
        context['tags'] = Thread.tags.all()
        context['order'] = self.order
        return context

index = ForumView.as_view()