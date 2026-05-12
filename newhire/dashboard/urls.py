from django.urls import path
from .views import DashboardIndexView, DashboardLoginView, DashboardLogoutView, DashboardPostCreateView, DashboardPostListView, DashboardPostEditView

app_name = 'dashboards'

dashboard_login_view = DashboardLoginView.as_view()
dashboard_logout_view = DashboardLogoutView.as_view()
dashboard_index_view = DashboardIndexView.as_view()
dashboard_post_list_view = DashboardPostListView.as_view()
dashboard_post_create_view = DashboardPostCreateView.as_view()
dashboard_post_edit_view = DashboardPostEditView.as_view()

urlpatterns = [
    path('login/', dashboard_login_view, name='login'),
    path('logout/', dashboard_logout_view, name='logout'),
    path('', dashboard_index_view, name='index'),
    path('posts/', dashboard_post_list_view, name='post-list'),
    path('posts/create/', dashboard_post_create_view, name='post-create'),
    path('posts/<int:pk>/edit/', dashboard_post_edit_view, name='post-edit'),
]
