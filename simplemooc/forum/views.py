from django.shortcuts import render
from django.views.generic import TemplateView, View

class ForumView(TemplateView):

    template_name = 'forum/index.html'


index = ForumView.as_view()