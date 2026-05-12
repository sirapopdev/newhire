from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.utils.translation import ngettext_lazy
from django_tables2 import A, Column, TemplateColumn

from oscar.core.loading import get_class

from newhire.blog.models import Post, Category

DashboardTable = get_class("dashboard.tables", "DashboardTable")


class PostTable(DashboardTable):
    checkbox = TemplateColumn(
        verbose_name="",
        template_code=(
            '<input type="checkbox" name="selected_post" '
            'class="selected_post" value="{{ record.id }}"/>'
        ),
        orderable=False,
    )
    title = TemplateColumn(
        template_code=(
            "<strong>{{ record.title }}</strong><br>"
            '<small class="text-muted">{{ record.slug }}</small>'
        ),
        verbose_name=_("Title"),
        order_by="title",
        accessor=A("title"),
    )
    image = TemplateColumn(
        verbose_name=_("Image"),
        template_code=(
            '<img src="{{ record.featured_image_url }}" '
            'alt="{{ record.title }}" '
            'style="width: 60px; height: 60px; object-fit: cover;">'
        ),
        orderable=False,
    )
    category = Column(
        verbose_name=_("Category"),
        accessor=A("category"),
        order_by="category__name",
    )
    author = Column(
        verbose_name=_("Author"),
        accessor=A("author"),
        orderable=False,
    )
    actions = TemplateColumn(
        template_name="dashboard/post/row_actions.html",
        verbose_name=_("Actions"),
        orderable=False,
    )

    icon = "fas fa-newspaper"
    caption = ngettext_lazy("%s Post", "%s Posts")

    class Meta(DashboardTable.Meta):
        model = Post
        fields = ("status", "updated_at")
        sequence = (
            "checkbox",
            "title",
            "image",
            "category",
            "status",
            "author",
            "updated_at",
            "actions",
        )
        order_by = "-updated_at"
        per_page = settings.OSCAR_DASHBOARD_ITEMS_PER_PAGE

    def render_category(self, record):
        return record.category.name if record.category else _("No category")

    def render_status(self, record):
        return record.get_status_display()

    def render_author(self, record):
        return record.author.name or record.author.email

class CategoryTable(DashboardTable):
    checkbox = TemplateColumn(
        verbose_name="",
        template_code=(
            '<input type="checkbox" name="selected_category" '
            'class="selected_category" value="{{ record.id }}"/>'
        ),
        orderable=False,
    )
    name = Column(
        verbose_name=_("Name"),
        accessor=A("name"),
        order_by="name",
    )
    actions = TemplateColumn(
        template_name="dashboard/category/row_actions.html",
        verbose_name=_("Actions"),
        orderable=False,
    )

    icon = "fas fa-folder"
    caption = ngettext_lazy("%s Category", "%s Categories")

    class Meta(DashboardTable.Meta):
        model = Category
        fields = ()
        sequence = (
            "checkbox",
            "name",
            "actions",
        )
        order_by = "name"
        per_page = settings.OSCAR_DASHBOARD_ITEMS_PER_PAGE
    