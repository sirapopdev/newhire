from django.urls import path
from .views import PostDetailView, PostListView

post_list_view = PostListView.as_view()
post_detail_view = PostDetailView.as_view()

urlpatterns = [
    path('', post_list_view, name='post-list'),
    path('<slug:slug>/', post_detail_view, name='post-detail'),
]
