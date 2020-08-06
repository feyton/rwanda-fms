from django.shortcuts import render
from django.views.generic import View
from .forms import UpdateProfileForm, UpdateUserForm
from .models import Profile


class UserProfile(View):
    def get(self, *args, **kwargs):
        user = self.request.user
        profile, created = Profile.objects.get_or_create(user=user)
        context = {
            'form': UpdateUserForm(instance=user),
            'p_form': UpdateProfileForm(instance=profile)
        }

        return render(self.request, 'user/profile.html', context)


profile_view = UserProfile.as_view()
