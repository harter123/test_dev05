import json
from django.contrib.auth.models import User, Group
from django.contrib import auth
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from app_common.utils.response import response_success, Error


class LoginView(APIView):
    #  这个接口的调用不能加认证
    authentication_classes = []

    def post(self, request):
        """
        登录账号，并获取token
        """
        login_username = request.data.get("username", "")
        login_password = request.data.get("password", "")
        if login_username == '' or login_password == '':
            return response_success(error=Error.USER_OR_PAWD_NULL)
        else:
            user = auth.authenticate(username=login_username, password=login_password)
            if user is not None and user.is_active:
                auth.login(request, user)  # 验证登录
                # update the token
                token = Token.objects.filter(user=user)
                token.delete()
                token = Token.objects.create(user=user)
                user_info = {
                    "id": user.id,
                    "name": login_username
                }
                user_str = json.dumps(user_info)
                return response_success(data={"Token": str(token), 'User': user_str})
            else:
                return response_success(error=Error.USER_OR_PAWD_ERROR)

    def delete(self, request):
        """
        退出账号，并删除token
        """
        userId = request.data.get("user")
        token = Token.objects.filter(user=userId)
        token.delete()
        return response_success()


class UsersView(APIView):
    #  这个接口的调用不能加认证
    authentication_classes = []

    def get(self, request):
        """
        登录账号，并获取token
        """
        users = User.objects.filter(is_active=True)
        ret = []
        for u in users:
            tmp = {
                "id": u.id,
                "name": u.username
            }
            ret.append(tmp)
        # ret = [{"id": u.id, "name": u.username} for u in users]
        return response_success(data=ret)
