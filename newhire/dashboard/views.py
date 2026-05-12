from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, TemplateView, UpdateView, DeleteView
from django_tables2 import SingleTableView

from newhire.blog.models import Post

from .forms import PostForm, PostSearchForm
from .tables import PostTable


class DashboardLoginView(LoginView):
    template_name = 'dashboard/login.html'
    redirect_authenticated_user = True

    def form_valid(self, form):
        user = form.get_user()

        if not user.is_staff:
            raise PermissionDenied

        return super().form_valid(form)

    def get_success_url(self):
        return self.get_redirect_url() or "/dashboard/"


class DashboardLogoutView(LogoutView):
    next_page = "/blogs/"


class StaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    login_url = "dashboards:login"

    def test_func(self):
        return self.request.user.is_staff


class DashboardIndexView(StaffRequiredMixin, TemplateView):
    template_name = 'dashboard/index.html'


class DashboardPostListView(
    StaffRequiredMixin, SingleTableView
):
    template_name = 'dashboard/post/list.html'
    model = Post
    table_class = PostTable
    context_table_name = "posts"
    form_class = PostSearchForm

    def get_queryset(self):
        self.form = self.form_class(self.request.GET)
        posts = Post.objects.select_related("category", "author").prefetch_related("tags")

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

    def get_table(self, **kwargs):
        table = super().get_table(**kwargs)
        table.caption = self.get_description()
        return table

    def get_description(self):
        if self.form.is_valid() and any(self.form.cleaned_data.values()):
            return _("Post search results")
        return _("Posts")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.form
        context["has_posts"] = self.object_list.exists()
        return context


class DashboardPostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "dashboard/post/form.html"
    login_url = "dashboards:login"
    success_url = reverse_lazy("dashboards:post-list")

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, _("Post created successfully."))
        return super().form_valid(form)
    
class DashboardPostEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = "dashboard/post/form.html"
    login_url = "dashboards:login"
    success_url = reverse_lazy("dashboards:post-list")

    def test_func(self):
        post = self.get_object()
        return self.request.user.is_staff or post.author == self.request.user

    def form_valid(self, form):
        messages.success(self.request, _("Post updated successfully."))
        return super().form_valid(form)


class DashboardPostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = "dashboard/post/confirm_delete.html"
    login_url = "dashboards:login"
    success_url = reverse_lazy("dashboards:post-list")

    def test_func(self):
        post = self.get_object()
        return self.request.user.is_staff or post.author == self.request.user

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, _("Post deleted successfully."))
        return super().delete(request, *args, **kwargs)