from django.contrib.auth.views import LoginView, LogoutView
from django.core.exceptions import PermissionDenied


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
