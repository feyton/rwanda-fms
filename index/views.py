from django.shortcuts import render
from django.views.generic import View


class Home(View):
    def get(self, *args, **kwargs):
        template = 'index.html'
        context = {
            'active': 'home'
        }
        return render(self.request, template, context)


home_view = Home.as_view()
