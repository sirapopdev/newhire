from django.urls import path
from .views import DashboardLoginView, DashboardLogoutView

app_name = 'dashboards'

dashboard_login_view = DashboardLoginView.as_view()
dashboard_logout_view = DashboardLogoutView.as_view()

urlpatterns = [
    path('login/', dashboard_login_view, name='login'),
    path('logout/', dashboard_logout_view, name='logout'),
]
