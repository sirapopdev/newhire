from django_tables2 import A, Column, TemplateColumn
from oscar.core.loading import get_class

from django.conf import settings
from django.utils.translation import gettext_lazy as _, ngettext_lazy

from newhire.blog.models import Category, Comment, Post

DashboardTable = get_class("dashboard.tables", "DashboardTable")


class PostTable(DashboardTable):
    title = TemplateColumn(
        template_name="dashboard/post/title_column.html",
        verbose_name=_("Title"),
        order_by="title",
        accessor=A("title"),
    )
    image = TemplateColumn(
        verbose_name=_("Image"),
        template_name="dashboard/post/image_column.html",
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
            "name",
            "actions",
        )
        order_by = "name"
        per_page = settings.OSCAR_DASHBOARD_ITEMS_PER_PAGE
    

class CommentTable(DashboardTable):
    body = Column(
        verbose_name=_("Comment"),
        accessor=A("body"),
        orderable=False,        
    )
    author = Column(
        verbose_name=_("Commenter"),
        accessor=A("author"),
        orderable=False,
    )
    post = Column(
        verbose_name=_("Post"),
        accessor=A("post"),
        orderable=False,
    )
  
    created_at = Column(
        verbose_name=_("Created At"),
        accessor=A("created_at"),
        order_by="created_at",
    )
    actions = TemplateColumn(
        template_name="dashboard/comment/row_actions.html",
        verbose_name=_("Actions"),
        orderable=False,
    )       

    icon = "fas fa-comments"
    caption = ngettext_lazy("%s Comment", "%s Comments")

    class Meta(DashboardTable.Meta):
        model = Comment
        fields = ()
        sequence = (
            "body",
            "author",
            "post",
            "created_at",
            "actions",
        )
        order_by = "-created_at"
        per_page = settings.OSCAR_DASHBOARD_ITEMS_PER_PAGE
