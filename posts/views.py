"""Posts views."""

# Django
from django.urls.base import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView,CreateView

# Forms
from posts.forms import PostForm

# Models
from posts.models import Post


class PostDetailView(LoginRequiredMixin, DetailView):
    template_name = 'posts/details.html'
    slug_field = 'id'
    slug_url_kwarg = 'post_id'
    queryset = Post.objects.all()


class PostsFeedView(LoginRequiredMixin,ListView):
    """Return all published posts."""

    template_name = 'posts/feed.html'
    model = Post
    ordering = ('-created',)
    paginate_by = 30
    context_object_name = 'posts'


class CreatePostView(LoginRequiredMixin,CreateView):
    """Create a new post."""

    template_name='posts/new.html'
    form_class = PostForm
    success_url = reverse_lazy('posts:feed')

    def get_context_data(self,**kargs):
        """Add users and profile to context."""
        context = super().get_context_data(**kargs)
        context['user']=self.request.user
        context['profile']=self.request.user.profile
        return context
