from django.shortcuts import render
from django.views.generic import FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from common.forms import ProfileCreationForm
from django.http.response import HttpResponseRedirect
from django.urls import reverse_lazy
from common.models import UserProfile
from allauth.socialaccount.models import SocialAccount


def index(request):
    context = {}
    if request.user.is_authenticated:
        context['username'] = request.user.username
        try:
            context['age'] = UserProfile.objects.get(user=request.user).age
        except:
            context['age'] = None

        try:
            context['github_url'] = SocialAccount.objects.get(provider='github', user=request.user).extra_data['html_url']
        except:
            context['github_url'] = None

    return render(request, 'index.html', context)


class RegisterView(FormView):
    form_class = UserCreationForm

    def form_valid(self, form):
        form.save()
        username = form.cleaned_data.get('username')
        raw_password = form.cleaned_data.get('password1')
        login(self.request, authenticate(username=username, password=raw_password))
        return super(RegisterView, self).form_valid(form)


class CreateUserProfile(FormView):
    form_class = ProfileCreationForm
    template_name = 'profile-create.html'
    success_url = reverse_lazy('common:index')

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_anonymous:
            return HttpResponseRedirect(reverse_lazy('common:login'))
        return super(CreateUserProfile, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = self.request.user
        instance.save()
        return super(CreateUserProfile, self).form_valid(form)


class EditUserProfile(FormView):
    form_class = ProfileCreationForm
    template_name = 'profile-update.html'
    success_url = reverse_lazy('common:index')

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_anonymous:
            return HttpResponseRedirect(reverse_lazy('common:login'))
        return super(EditUserProfile, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        try:
            instance = self.request.user
            user = UserProfile.objects.get(user=instance)
            user.age = form.cleaned_data.get('age')
            user.save()
        except:
            instance = form.save(commit=False)
            instance.user = self.request.user
            instance.save()
        return super(EditUserProfile, self).form_valid(form)




