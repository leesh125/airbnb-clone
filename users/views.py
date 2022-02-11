from django.views import View
from django.shortcuts import render
from . import forms


class LoginView(View):
    def get(self, request):
        form = forms.LoginForm()  # form 추가 후 view에 넘겨주기
        return render(request, "users/login.html", {"form": form})

    def post(self, request):
        form = forms.LoginForm(request.POST)
        if form.is_valid():  # 유효한 email과 password가 들어왔으면
            print(form.cleaned_data)
        return render(request, "users/login.html", {"form": form})