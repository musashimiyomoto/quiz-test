from django.contrib.auth import (login,
                                 logout,
                                 authenticate)
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView


class LogIn(LoginView):
    template_name = 'index.html'

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')
        rememberme = request.POST.get('rememberme')

        user_obj = User.objects.filter(username=username).first()
        if user_obj is None:
            messages.success(request=request, message="Пользователь не найден!!!")
            return redirect('login')

        user = authenticate(username=username, password=password)
        if user is None:
            messages.success(request=request, message="Введен неверный пароль")
            return redirect('login')

        login(request=request, user=user)

        if not rememberme:
            self.request.session.set_expiry(0)
            self.request.session.modified = True

        messages.success(request=request, message="Success")

        return redirect('quiz/')


class SignUp(CreateView):
    model = User
    fields = "__all__"
    template_name = 'register.html'
    success_url = reverse_lazy('login')

    def post(self, request, *args, **kwargs):
        try:
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')
            username = request.POST.get('username')
            email = request.POST.get('email')
            first_name = request.POST.get('firstname')
            last_name = request.POST.get('lastname')

            if password1 != password2:
                messages.success(request, 'Пароли в обоих полях паролей не совпадают!!!')
                return redirect('signup')

            if User.objects.filter(username=username).first():
                messages.success(request, "Этот пользователь уже зарегистрирован!!!")
                return redirect('signup')

            if User.objects.filter(email=email).first():
                messages.success(request, "Эта электронная почта уже зарегистрирована!!!")
                return redirect('signup')

            user_obj = User.objects.create(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name
            )
            user_obj.set_password(raw_password=password1)
            user_obj.save()
            return redirect('login')
        except Exception as e:
            messages.error(request, f"Ошибка {e}")
            return redirect('signup')


def user_logout(request):
    logout(request)
    return redirect(to='login')
