from django.shortcuts import render
from django.views.generic import View


class UserProfile(View):
    def get(self, *args, **kwargs):
        user = self.request.user
        profile = self.request.user.profile
        context = {
            'form'
        }

