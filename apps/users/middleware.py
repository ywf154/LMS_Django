from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import resolve, reverse


class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path in ['/login/', '/register/']:
            return self.get_response(request)
        if request.path != reverse('login') and request.path != reverse('register'):
            if not request.user.is_authenticated:
                # 如果未登录,则重定向到登录页面
                return redirect(reverse('login'))
        return self.get_response(request)