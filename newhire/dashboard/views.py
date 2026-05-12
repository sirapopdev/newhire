from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, UpdateView, DeleteView
from django_tables2 import SingleTableView

from newhire.blog.models import Category, Post, Comment

from .forms import CategoryForm, CategorySearchForm, PostForm, PostSearchForm
from .tables import CategoryTable, CommentTable, PostTable

class DashboardPostListView(
    LoginRequiredMixin, SingleTableView
):
    template_name = 'dashboard/post/list.html'
    model = Post
    table_class = PostTable
    context_table_name = "posts"
    form_class = PostSearchForm

    def get_queryset(self):
        self.form = self.form_class(self.request.GET)
        posts = Post.objects.select_related("category", "author").prefetch_related("tags")

        if not self.request.user.is_staff:
            posts = posts.filter(author=self.request.user)

        if self.form.is_valid():
            query = self.form.cleaned_data.get("q")
            if query:
                posts = posts.filter(
                    Q(title__icontains=query)
                    | Q(body__icontains=query)
                    | Q(author__name__icontains=query)
                )

        return posts

    def get_table_pagination(self, table):
        return {"per_page": settings.OSCAR_DASHBOARD_ITEMS_PER_PAGE}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.form
        context["has_posts"] = self.object_list.exists()
        return context


class DashboardPostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "dashboard/post/form.html"
    login_url = "account_login"
    success_url = reverse_lazy("dashboard_blogs:post-list")

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, _("Post created successfully."))
        return super().form_valid(form)
    
class DashboardPostEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = "dashboard/post/form.html"
    login_url = "account_login"
    success_url = reverse_lazy("dashboard_blogs:post-list")

    def test_func(self):
        post = self.get_object()
        return self.request.user.is_staff or post.author == self.request.user

    def form_valid(self, form):
        messages.success(self.request, _("Post updated successfully."))
        return super().form_valid(form)


class DashboardPostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = "dashboard/post/confirm_delete.html"
    login_url = "account_login"
    success_url = reverse_lazy("dashboard_blogs:post-list")

    def test_func(self):
        post = self.get_object()
        return self.request.user.is_staff or post.author == self.request.user

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, _("Post deleted successfully."))
        return super().delete(request, *args, **kwargs)
    

class DashboardCategoryListView(LoginRequiredMixin, SingleTableView):
    template_name = 'dashboard/category/list.html'
    model = Category
    table_class = CategoryTable
    context_table_name = "categories"
    form_class = CategorySearchForm

    def get_queryset(self):
        self.form = self.form_class(self.request.GET)
        categories = Category.objects.all()

        if self.form.is_valid():
            query = self.form.cleaned_data.get("q")
            if query:
                categories = categories.filter(name__icontains=query)

        return categories

    def get_table_pagination(self, table):
        return {"per_page": settings.OSCAR_DASHBOARD_ITEMS_PER_PAGE}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.form
        context["has_categories"] = self.object_list.exists()
        return context
    
class DashboardCategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = "dashboard/category/form.html"
    login_url = "account_login"
    success_url = reverse_lazy("dashboard_blogs:category-list")

    def form_valid(self, form):
        messages.success(self.request, _("Category created successfully."))
        return super().form_valid(form)
    
class DashboardCategoryEditView(LoginRequiredMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = "dashboard/category/form.html"
    login_url = "account_login"
    success_url = reverse_lazy("dashboard_blogs:category-list")

    def test_func(self):
        return self.request.user.is_staff

    def form_valid(self, form):
        messages.success(self.request, _("Category updated successfully."))
        return super().form_valid(form)
    

class DashboardCategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = Category
    template_name = "dashboard/category/confirm_delete.html"
    login_url = "account_login"
    success_url = reverse_lazy("dashboard_blogs:category-list")


    def test_func(self):
        category = self.get_object()
        return self.request.user.is_staff or category.author == self.request.user

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, _("Category deleted successfully."))
        return super().delete(request, *args, **kwargs)
    
class DashboardCommentListView(LoginRequiredMixin, SingleTableView):
    template_name = 'dashboard/comment/list.html'
    model = Comment
    table_class = CommentTable
    context_table_name = "comments"

    def get_queryset(self):
        return Comment.objects.select_related("post", "author").filter(post__author=self.request.user)

    def get_table_pagination(self, table):
        return {"per_page": settings.OSCAR_DASHBOARD_ITEMS_PER_PAGE}
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["has_comments"] = self.object_list.exists()
        return context
    
class DashboardCommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = "dashboard/comment/confirm_delete.html"
    login_url = "account_login"
    success_url = reverse_lazy("dashboard_blogs:comment-list")

    def test_func(self):
        comment = self.get_object()
        return comment.author == self.request.user or self.request.user.is_staff

