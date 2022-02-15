import os
import requests
from django.views import View
from django.views.generic import FormView, DetailView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from django.core.files.base import ContentFile
from django.contrib import messages
from . import forms, models


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
        # 이메일 인증 한 사람만 로그인 하게끔(custom)
        # check_user = models.User.objects.get(username=user)

        # if check_user.email_verified == False:
        #     print("please verify your email")
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)


def log_out(request):
    messages.info(request, "See you later")
    logout(request)
    return redirect(reverse("core:home"))


class SingUpView(FormView):
    template_name = "users/signup.html"
    form_class = forms.SignUpForm
    success_url = reverse_lazy("core:home")

    def form_valid(self, form):  # form이 에러없이 유효하다면
        form.save()  # user를 생성하는 메소드
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)

        user.verify_email()
        return super().form_valid(form)


# 이메일 인증을 완료한 후 페이지
def complete_verification(request, key):
    try:
        # 해당 secret key 메일을 받은 user를 찾는다
        user = models.User.objects.get(email_secret=key)
        user.email_verified = True
        user.email_secret = ""  # 이메일 인증이 끝나면 secret 초기화
        user.save()
        # to do: add success message
    except models.User.DoesNotExist:
        # to do: add error message
        pass
    return redirect(reverse("core:home"))


# 로그인 역할을 github로 보냄
def github_login(request):
    client_id = os.environ.get("GH_ID")
    redirect_uri = "http://127.0.0.1:8000/users/login/github/callback"

    return redirect(  # github 인증을 요청하기 위해 request
        f"https://github.com/login/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&scope=read:user"
    )


class GithubException(Exception):
    pass


# github에서 인증이 끝난 후 호출
def github_callback(request):
    try:
        client_id = os.environ.get("GH_ID")
        client_secret = os.environ.get("GH_SECRET")
        code = request.GET.get("code", None)
        if code is not None:
            # github에 request를 보내서 code를 가지고 access_token을 얻는다
            token_request = requests.post(
                f"https://github.com/login/oauth/access_token?client_id={client_id}&client_secret={client_secret}&code={code}",
                headers={"Accept": "application/json"},
            )
            token_json = token_request.json()
            error = token_json.get("error", None)
            if error is not None:
                raise GithubException("Can't get access token")
            else:
                access_token = token_json.get("access_token")
                profile_request = requests.get(
                    "https://api.github.com/user",
                    headers={
                        "Authorization": f"token {access_token}",
                        "Accept": "application/json",
                    },
                )
                profile_json = profile_request.json()
                username = profile_json.get("login", None)
                if username is not None:
                    name = profile_json.get("name")
                    email = profile_json.get("email")
                    bio = profile_json.get("bio")
                    try:
                        user = models.User.objects.get(email=email)
                        if user.login_method != models.User.LOGIN_GITHUB:
                            raise GithubException(
                                f"Please log in with: {user.login_method}"
                            )
                    except models.User.DoesNotExist:
                        user = models.User.objects.create(
                            email=email,
                            first_name=name,
                            username=email,
                            bio=bio,
                            login_method=models.User.LOGIN_GITHUB,
                            email_verified=True,
                        )
                        user.set_unusable_password()
                        user.save()
                    login(request, user)
                    messages.success(request, f"Welcome back {user.first_name}")
                    return redirect(reverse("core:home"))
                else:
                    raise GithubException("Can't get your profile")
        else:
            raise GithubException("Can't get code")
    except GithubException as e:
        messages.error(request, e)


# kakao 로그인 요청
def kakao_login(request):
    client_id = os.environ.get("KAKAO_ID")  # 앱 REST API 키
    redirect_uri = (
        "http://127.0.0.1:8000/users/login/kakao/callback"  # 인가 코드가 리다이렉트될 URI
    )
    return redirect(
        f"https://kauth.kakao.com/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code"
    )


class KakaoException(Exception):
    pass


def kakao_callback(request):
    try:
        code = request.GET.get("code")  # 인가 코드 받기 요청으로 얻은 인가 코드
        client_id = os.environ.get("KAKAO_ID")  # 	앱 REST API 키
        redirect_uri = (
            "http://127.0.0.1:8000/users/login/kakao/callback"  # 인가 코드가 리다이렉트된 URI
        )
        token_request = requests.get(
            f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={client_id}&redirect_uri={redirect_uri}&code={code}"
        )
        token_json = token_request.json()  # 토큰 json 얻기
        error = token_json.get("error", None)
        if error is not None:  # 에러가 발생했다면 예외
            raise KakaoException("Can't get authorization code.")
        access_token = token_json.get("access_token")  # access_token 값 얻기
        profile_request = requests.get(  # 액세스 토큰으로 kakao user 정보 얻기
            "https://kapi.kakao.com/v2/user/me",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        profile_json = profile_request.json()  # kakao user의 profile을 json 형식으로 받음
        email = profile_json.get("kakao_account").get("email")
        if email is None:
            raise KakaoException("Please also give me your email")
        properties = profile_json.get("properties")  # json에서 사용자의 정보 얻기
        nickname = properties.get("nickname")
        profile_image = (
            profile_json.get("kakao_account").get("profile").get("profile_image_url")
        )
        try:
            # 이미 카카오 id의 email과 같은 아이디가 db에 있는지
            user = models.User.objects.get(email=email)
            # 해당 user(중복 email)의 login_method가 kakao로 로그인 되어있는게 아니라면 예외
            if user.login_method != models.User.LOGIN_KAKAO:
                raise KakaoException(f"Please log in with: {user.login_method}")
        except models.User.DoesNotExist:  # 카카오로 로그인한 email이 db에 없다면
            user = models.User.objects.create(  # 주어진 정보로 user 생성
                email=email,
                username=email,
                first_name=nickname,
                login_method=models.User.LOGIN_KAKAO,
                email_verified=True,
            )
            user.set_unusable_password()
            user.save()
            if profile_image is not None:  # 프사가 있으면 얻기
                photo_request = requests.get(profile_image)

                user.avatar.save(
                    # file.save(파일 이름, 이미지 파일)
                    # ContentFile: 바이트코드로 이루어진 파일을 처리
                    f"{nickname}-avatar.jpg",
                    ContentFile(photo_request.content),
                )
        login(request, user)
        messages.success(request, f"Welcome back {user.first_name}")
        return redirect(reverse("core:home"))
    except KakaoException as e:
        messages.error(request, e)
        return redirect(reverse("users:login"))


class UserProfileView(DetailView):

    model = models.User
    context_object_name = "user_obj"