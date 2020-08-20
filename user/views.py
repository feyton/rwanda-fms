from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views.generic import View

from .forms import UpdateProfileForm, UpdateUserForm
from .models import Profile


@method_decorator(login_required, name='dispatch')
class UserProfile(View):
    def get(self, *args, **kwargs):
        user = self.request.user
        profile, created = Profile.objects.get_or_create(user=user)
        context = {
            'form': UpdateUserForm(instance=user),
            'p_form': UpdateProfileForm(instance=profile)
        }

        return render(self.request, 'user/profile.html', context)

    def post(self, *args, **kwargs):
        user = self.request.user
        profile, created = Profile.objects.get_or_create(user=user)
        form= UpdateUserForm(self.request.POST or None, instance=user)
        p_form = UpdateProfileForm(self.request.POST or None, self.request.FILES or None, instance=profile)

        if form.is_valid() and p_form.is_valid():
            form.save()
            p_form.save()
            messages.info(self.request, 'Your profile has been successfully updated')
            return redirect('user-profile')
        else:
            messages.error(self.request, 'Please fill the form correctly')
            return redirect('user-profile')


profile_view = UserProfile.as_view()
