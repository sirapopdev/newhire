from django.urls import path
from .views import CategoryPostListView, PostDetailView, PostListView, TagPostListView

post_list_view = PostListView.as_view()
category_post_list_view = CategoryPostListView.as_view()
tag_post_list_view = TagPostListView.as_view()
post_detail_view = PostDetailView.as_view()

urlpatterns = [
    path('', post_list_view, name='post-list'),
    path('category/<slug:slug>/', category_post_list_view, name='post-category'),
    path('tag/<slug:slug>/', tag_post_list_view, name='post-tag'),
    path('<slug:slug>/', post_detail_view, name='post-detail'),
]
