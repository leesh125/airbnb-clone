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


class SignUpForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = ("first_name", "last_name", "email")

    password = forms.CharField(widget=forms.PasswordInput)
    password1 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    def clean_password1(self):
        password = self.cleaned_data.get("password1")
        password1 = self.cleaned_data.get("password1")

        if password != password1:
            raise forms.ValidationError("Password confirmation does not match")
        else:
            return password

    def save(self, *args, **kwargs):
        user = super().save(commit=False)  # user object는 생성하지만 db에는 올리지 않음
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        user.username = email # email을 username으로 저장
        user.set_password(password) # 암호화된 패스워드를 적용
        user.save()
