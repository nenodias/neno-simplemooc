from django.shortcuts import render
from django.views.generic import TemplateView, View, ListView

class ForumView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'forum/index.html')


index = ForumView.as_view()