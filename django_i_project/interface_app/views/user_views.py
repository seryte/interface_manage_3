import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render

# Create your views here.
from django.views.decorators.http import require_http_methods

from interface_app.forms.user_from import UserForm
from interface_app.libs.respone import response_failed, ErrorCode, response_success


@require_http_methods(['POST'])
def user_login(request, *args, **kwargs):
    """
    登录
    :param request:
    :param args:
    :param kwargs:
    :return:
    """
    body = request.body
    data = json.loads(body, encoding='utf-8')

    user_form = UserForm(data)

    if not user_form.is_valid():
        return response_failed()

    # username = data.get("username", "")
    # password = data.get("password", "")
    #
    # if not username or not password:
    #     return response_failed()

    # authenticate函数是用来校验用户名密码是否正常
    user = authenticate(username=user_form.cleaned_data['username'], password=user_form.cleaned_data['password'])
    if not user:
        return response_failed(code=ErrorCode.auth, message="登录失败")
    else:
        login(request, user)
        return response_success()


@require_http_methods(['POST'])
def user_register(request, *args, **kwargs):
    body = request.body
    data = json.loads(body, encoding='utf-8')

    user_form = UserForm(data)

    if not user_form.is_valid():
        return response_failed()
    username = user_form.cleaned_data['username']
    password = user_form.cleaned_data['password']
    #
    # if not username or not password:
    #     return response_failed()

    if User.objects.filter(username=username).exists():
        return response_failed(code=ErrorCode.auth, message="用户名已存在")

    user = User.objects.create_user(username=username, password=password)
    if not user:
        return response_failed(code=ErrorCode.auth, message="注册失败")
    else:
        login(request, user)
        return response_success()


@require_http_methods(['DELETE'])
def user_logout(request, *args, **kwargs):
    logout(request)
    return response_success()


@require_http_methods(['GET'])
def get_user_info(request, *args, **kwargs):
    """
    获取已登录的用户信息
    :param request:
    :param args:
    :param kwargs:
    :return:
    """
    user = request.user
    print(user)
    if not user:
        return response_failed(code=ErrorCode.auth, message="用户未登录")
    # 判断用户是否已通过校验
    if user.is_authenticated:
        return response_success(data={
            "id": user.id,
            "name": user.username
        })
    else:
        return response_failed(code=ErrorCode.auth, message="用户未登录")
