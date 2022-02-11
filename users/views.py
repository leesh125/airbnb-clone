from django.views import View
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from . import forms


class LoginView(FormView):

    template_name = "users/login.html"
    form_class = forms.LoginForm
    # url을 통해 클래스(뷰)를 불러올때 아직 url은 불려지지 않음
    # reverse_lazy를 통해 이미 요청 응답이 끝난 페이지에서 다른 페이지로 가고자 할 때
    # 뒤늦게 호출할 수 있다.(로그인 버튼을 누르면 동일한 url로 POST방식으로 전달 후 홈으로 REDIRECT)
    success_url = reverse_lazy("core:home")

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)


def log_out(request):
    logout(request)
    return redirect(reverse("core:home"))
