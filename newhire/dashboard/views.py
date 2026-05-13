from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, UpdateView, DeleteView
from django_filters.views import FilterView
from django_tables2 import SingleTableMixin, SingleTableView
from oscar.apps.dashboard.views import IndexView as OscarIndexView

from newhire.blog.models import Category, Post, Comment

from .filters import CategoryFilter, PostFilter
from .forms import CategoryForm, PostForm
from .tables import CategoryTable, CommentTable, PostTable


class IndexView(OscarIndexView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_posts"] = Post.objects.count()
        context["total_categories"] = Category.objects.count()
        context["total_comments"] = Comment.objects.count()
        return context


class DashboardPostListView(
    LoginRequiredMixin, SingleTableMixin, FilterView
):
    template_name = 'dashboard/post/list.html'
    model = Post
    table_class = PostTable
    context_table_name = "posts"
    filterset_class = PostFilter

    def get_queryset(self):
        return Post.objects.select_related("category", "author").prefetch_related("tags")

    def get_table_pagination(self, table):
        return {"per_page": settings.OSCAR_DASHBOARD_ITEMS_PER_PAGE}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.filterset.form
        context["has_posts"] = self.object_list.exists()
        return context


class DashboardPostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "dashboard/post/form.html"
    success_url = reverse_lazy("dashboard_blogs:post-list")

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, _("Post created successfully."))
        return super().form_valid(form)
    
class DashboardPostEditView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = "dashboard/post/form.html"
    success_url = reverse_lazy("dashboard_blogs:post-list")

    def form_valid(self, form):
        messages.success(self.request, _("Post updated successfully."))
        return super().form_valid(form)


class DashboardPostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = "dashboard/post/confirm_delete.html"
    success_url = reverse_lazy("dashboard_blogs:post-list")

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, _("Post deleted successfully."))
        return super().delete(request, *args, **kwargs)
    

class DashboardCategoryListView(LoginRequiredMixin, SingleTableMixin, FilterView):
    template_name = 'dashboard/category/list.html'
    model = Category
    table_class = CategoryTable
    context_table_name = "categories"
    filterset_class = CategoryFilter

    def get_queryset(self):
        return Category.objects.all()

    def get_table_pagination(self, table):
        return {"per_page": settings.OSCAR_DASHBOARD_ITEMS_PER_PAGE}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.filterset.form
        context["has_categories"] = self.object_list.exists()
        return context
    
class DashboardCategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = "dashboard/category/form.html"
    success_url = reverse_lazy("dashboard_blogs:category-list")

    def form_valid(self, form):
        messages.success(self.request, _("Category created successfully."))
        return super().form_valid(form)
    
class DashboardCategoryEditView(LoginRequiredMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = "dashboard/category/form.html"
    success_url = reverse_lazy("dashboard_blogs:category-list")

    def form_valid(self, form):
        messages.success(self.request, _("Category updated successfully."))
        return super().form_valid(form)
    

class DashboardCategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = Category
    template_name = "dashboard/category/confirm_delete.html"
    success_url = reverse_lazy("dashboard_blogs:category-list")

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
    
class DashboardCommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment
    template_name = "dashboard/comment/confirm_delete.html"
    success_url = reverse_lazy("dashboard_blogs:comment-list")
