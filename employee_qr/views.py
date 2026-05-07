from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect


class AdminLoginView(LoginView):
    template_name = "registration/login.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_staff:
            return redirect(self.get_success_url())
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.get_user()
        if not user.is_staff:
            messages.error(self.request, "Only admin users can access the management dashboard.")
            return redirect("login")
        return super().form_valid(form)
