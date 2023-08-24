from django.contrib.auth.mixins import LoginRequiredMixin

class LoginRequiredViewMixin(LoginRequiredMixin):
    login_url = '/login'
    redirect_field_name = 'next'
