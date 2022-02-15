from django.shortcuts import redirect, reverse
from django.contrib.auth.mixins import UserPassesTestMixin

# 로그인 상태가 아닌 사람들만 볼 수 있게 하기위해(UserPassesTestMixin를 통해 알 수 있음)
class LoggedOutOnlyView(UserPassesTestMixin):

    permisson_denied_message = "Page not found"

    # user가 로그인 안했는지를 체크    
    def test_func(self):
        return not self.request.user.is_authenticated

    # 로그인을 안했는데 권한이 필요한 페이지를 간다면 홈으로
    def handle_no_permission(self):
        return redirect("core:home")
