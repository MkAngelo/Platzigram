"""Users views."""

# Django
import json
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import views as auth_views
from django.http import response, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, FormView, UpdateView
from django.views.generic.edit import UpdateView

# Forms
from users.forms import SignupForm
from posts.models import Post
from users.models import Profile, Following

# Models
from django.contrib.auth.models import User


class UserDetailView(LoginRequiredMixin ,DetailView):
    """User Detail View."""

    template_name = 'users/detail.html'
    slug_field = 'username'
    slug_url_kwarg = 'username'
    queryset = User.objects.all()
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        """Add user's posts to context."""
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        context['posts'] = (
            Post.objects.filter(user=user).order_by('-created')
        )
        return context


class UpdateProfileView(LoginRequiredMixin,UpdateView):
    """Update profile view."""

    template_name = 'users/update_profile.html'
    model =  Profile
    fields = ['website','biography','phone_number','picture']

    def get_object(self):
        """Return user's profile."""
        return self.request.user.profile
    
    def get_success_url(self):
        """Return to user's profile."""
        username = self.object.user.username
        return reverse('users:detail',kwargs={'username':username})


class LoginView(auth_views.LoginView):
    """Login view."""

    template_name = 'users/login.html'


class SignupView(FormView):
    """Users sign up view."""

    template_name = 'users/signup.html'
    form_class = SignupForm
    success_url = reverse_lazy('users:login')
    
    def form_valid(self,form):
        form.save()
        return super().form_valid(form)


class LogoutView(LoginRequiredMixin,auth_views.LogoutView):
    """Logout view."""

    template_name = 'users/logout.html'

@login_required
def follow(request,username):
    main_user = request.user
    to_follow = User.objects.get(username = username)
    following = Following.objects.filter(user=main_user,followed=to_follow)
    is_following = True if following else False

    if is_following:
        Following.unfollow(main_user,to_follow)
        is_following = False

    else:
        Following.follow(main_user,to_follow)
        is_following = True
    
    return redirect('users:detail',username)