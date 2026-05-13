from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic.edit import FormMixin
from django.views.generic.edit import ProcessFormView
from django.views.generic import DeleteView, DetailView, ListView
from django.db.models import Q
from .models import Category, Post, Comment
from .forms import CommentForm, PostFilterForm

class PostListView(ListView):
    model = Post
    template_name = 'blog/list.html'
    context_object_name = "posts"
    paginate_by = 10

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
        context.update({
            'blog_categories': Category.objects.all(),
            'recent_posts': Post.objects.all()[:5],
        })
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


class PostDetailView(FormMixin, DetailView, ProcessFormView):
    model = Post
    template_name = 'blog/detail.html'
    form_class = CommentForm

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('account_login')

        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.post = self.object
        comment.author = self.request.user
        comment.save()
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.get_absolute_url()
    

class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment

    def get_success_url(self):
        return self.object.post.get_absolute_url()
