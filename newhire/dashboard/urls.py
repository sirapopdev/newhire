from django.urls import path

from .views import (DashboardCategoryCreateView, DashboardCategoryDeleteView,
                    DashboardCategoryEditView, DashboardCategoryListView,
                    DashboardCommentDeleteView, DashboardCommentListView,
                    DashboardPostCreateView, DashboardPostDeleteView,
                    DashboardPostEditView, DashboardPostListView)

app_name = 'dashboard_blogs'

dashboard_post_list_view = DashboardPostListView.as_view()
dashboard_post_create_view = DashboardPostCreateView.as_view()
dashboard_post_edit_view = DashboardPostEditView.as_view()
dashboard_post_delete_view = DashboardPostDeleteView.as_view()
dashboard_category_list_view = DashboardCategoryListView.as_view()
dashboard_category_create_view = DashboardCategoryCreateView.as_view()
dashboard_category_edit_view = DashboardCategoryEditView.as_view()
dashboard_category_delete_view = DashboardCategoryDeleteView.as_view()
dashboard_comment_list_view = DashboardCommentListView.as_view()
dashboard_comment_delete_view = DashboardCommentDeleteView.as_view()

urlpatterns = [
    path('posts/', dashboard_post_list_view, name='post-list'),
    path('posts/create/', dashboard_post_create_view, name='post-create'),
    path('posts/<int:pk>/edit/', dashboard_post_edit_view, name='post-edit'),
    path('posts/<int:pk>/delete/', dashboard_post_delete_view, name='post-delete'),
    path('categories/', dashboard_category_list_view, name='category-list'),
    path('categories/create/', dashboard_category_create_view, name='category-create'),
    path('categories/<int:pk>/edit/', dashboard_category_edit_view, name='category-edit'),
    path('categories/<int:pk>/delete/', dashboard_category_delete_view, name='category-delete'),
    path('comments/', dashboard_comment_list_view, name='comment-list'),
    path('comments/<int:pk>/delete/', dashboard_comment_delete_view, name='comment-delete'),
]
