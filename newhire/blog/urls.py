from django.urls import path
from .views import PostListView

post_list_view = PostListView.as_view()

urlpatterns = [
    path('', post_list_view, name='post-list'),
]