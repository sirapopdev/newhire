from django.views.generic import DetailView, ListView
from .models import Post


# Create your views here.
class PostListView(ListView):
    model = Post
    template_name = 'blog/list.html'


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
