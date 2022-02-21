from django.contrib import messages
from django.shortcuts import redirect, reverse
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.urls import reverse_lazy


class EmailLoginOnlyView(UserPassesTestMixin):

    # kakao, github가 아닌 순수 회원가입을 한 유저인지 체크
    def test_func(self):
        return self.request.user.login_method == "email"

    def handle_no_permission(self):
        messages.error(self.request, _("Can't go there"))
        return redirect("core:home")


# 로그인 상태가 아닌 사람들만 볼 수 있게 하기위해(UserPassesTestMixin를 통해 알 수 있음)
class LoggedOutOnlyView(UserPassesTestMixin):

    # user가 로그인 안했는지를 체크
    def test_func(self):
        return not self.request.user.is_authenticated

    # 로그인을 안했는데 권한이 필요한 페이지를 간다면 홈으로
    def handle_no_permission(self):
        messages.error(self.request, _("Can't go there"))
        return redirect("core:home")


class LoggedInOnlyView(LoginRequiredMixin):
    # 로그인 안한 사람이 권한이 필요한 페이지로 이동하고자 한다면 login 페이지로 이동
    login_url = reverse_lazy("users:login")