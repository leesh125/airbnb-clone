from django import forms
from . import models


class LoginForm(forms.Form):

    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    # clean_data : 모든 field를 정리해준 것에 대한 결과이다.
    # clean_data() 의 경우 return 값을 지정하지 않으면 field를 지워버린다
    def clean_email(self):
        email = self.cleaned_data.get("email")  # email 필드 parameter를 가져옴
        try:
            models.User.objects.get(username=email)  # db에서 찾기
            return email
        except models.User.DoesNotExist:
            raise forms.ValidationError("User does not exist")

    def clean_password(self):
        print("clean email")