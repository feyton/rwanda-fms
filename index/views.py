from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

@method_decorator(login_required, name='dispatch')
class Home(View):
    def get(self, *args, **kwargs):
        template = 'index.html'
        context = {
            'active': 'home'
        }
        return render(self.request, template, context)


home_view = Home.as_view()
