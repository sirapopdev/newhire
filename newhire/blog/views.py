from django.views.generic import DetailView, ListView
from django.db.models import Q
from .models import Category, Post, Tag
from .forms import PostFilterForm

class PostListView(ListView):
    model = Post
    template_name = 'blog/list.html'
    paginate_by = 10

    def get_blog_sidebar_context(self):
        return {
            'blog_categories': Category.objects.all(),
            'recent_posts': Post.objects.all()[:5],
        }

    def get_queryset(self):
        self.form = PostFilterForm(self.request.GET)
        posts = Post.objects.all()

        if self.form.is_valid():
            query = self.form.cleaned_data.get('q')
            if query:
                posts = posts.filter(
                    Q(title__icontains=query) |
                    Q(body__icontains=query) |
                    Q(author__name__icontains=query) 
                )

        return posts

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_blog_sidebar_context())
        context['form'] = self.form
        return context


class CategoryPostListView(PostListView):
    def get_queryset(self):
        self.form = PostFilterForm(self.request.GET)
        posts = Post.objects.filter(category__slug=self.kwargs['slug'])
        if self.form.is_valid():
            query = self.form.cleaned_data.get('q')
            if query:
                posts = posts.filter(title__icontains=query)

        return posts

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['selected_category_slug'] = self.kwargs['slug']
        return context


class TagPostListView(PostListView):
    def get_queryset(self):
        self.form = PostFilterForm(self.request.GET)
        posts = Post.objects.filter(tags__slug=self.kwargs['slug'])

        if self.form.is_valid():
            query = self.form.cleaned_data.get('q')
            if query:
                posts = posts.filter(title__icontains=query)

        return posts

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['selected_tag_slug'] = self.kwargs['slug']
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
