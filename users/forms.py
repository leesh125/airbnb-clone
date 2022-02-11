from django import forms
from . import models


class LoginForm(forms.Form):

    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    # clean()을 통해 에러 공통처리
    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        try:
            user = models.User.objects.get(email=email)  # db에서 찾기
            if user.check_password(password):  # 해당 email을 가진 user model에서 password 체크
                return self.cleaned_data
            else:
                # add_error("필드", 에러): 해당 에러가 발생한 곳에서 에러 메시지 추가
                self.add_error("password", forms.ValidationError("Password is wrong"))
        except models.User.DoesNotExist:
            self.add_error("email", forms.ValidationError("User does not exist"))
