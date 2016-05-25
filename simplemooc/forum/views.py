from django.shortcuts import render
from django.views.generic import TemplateView, View, ListView, DetailView
from django.contrib import messages
from .forms import ReplyForm

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

class ThreadView(DetailView):

    model = Thread
    template_name = 'forum/thread.html'

    def get_context_data(self, **kwargs):
        context = super(ThreadView, self).get_context_data(**kwargs)
        context['tags'] = Thread.tags.all()
        context['form'] = ReplyForm(self.request.POST or None )
        return context

    def post(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated():
            messages.error(
                self.request,
                'Para responder ao tópico é necessário estar logado'
            )
            return redirect(self.request.path)
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        form = context['form']
        if form.is_valid():
            reply = form.save(commit=False)
            reply.thread = self.object
            reply.author = self.request.user
            reply.save()
            messages.success(self.request, 'A sua resposta foi enviada com sucesso')
            context['form'] = ReplyForm()
        return self.render_to_response(context)

index = ForumView.as_view()
thread = ThreadView.as_view()