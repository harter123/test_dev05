import json
from rest_framework import exceptions
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework.response import Response
from app_common.utils.response import Error
from rest_framework.authtoken.models import Token


class BaseView:

    def response_fail(self, error=""):
        """
        返回失败, 主要用于参数验证失败
        """
        error_msg = {
            "30010": str(error)
        }
        return self.response_success(success=False, error=error_msg, data=[])

    @staticmethod
    def response_success(success: bool = True, message: str = "", error={}, data: any = []) -> Response:
        """
        自定义接口返回格式
        """
        if error == {}:
            error_code = ""
            error_msg = ""
        else:
            success = False
            error_code = list(error.keys())[0]
            error_msg = list(error.values())[0]

        resp = {
            "success": success,
            "message": message,
            "error": {
                "code": error_code,
                "message": error_msg
            },
            "data": data
        }
        return Response(resp)

    @staticmethod
    def json_to_dict(json_str):
        """
        json to dict
        """
        if json_str == "":
            ret = dict()
            return ret

        try:
            ret = json.loads(json_str)
            if isinstance(ret, dict) is False:
                return None
        except json.decoder.JSONDecodeError as e:
            print("error", e)
            return None
        return ret

    def get_user(self, request):
        # 1. 在请求头的query_params中获取token
        # token = request.query_params.get('token')

        # 2. 直接在请求头中获取token

        # 3.直接获取uer
        header_token = request.META.get("HTTP_TOKEN", "")

        if header_token == "":
            raise exceptions.AuthenticationFailed("token为空")

        token = Token.objects.filter(key=header_token).first()
        if not token:
            raise exceptions.AuthenticationFailed("token认证失败")

        return token.user

class BaseAPIView(APIView, BaseView, Error):
    """
    继承APIView，
    Response：自定义返回格式
    Error: 自定义错误信息
    """
    pass


class BaseViewSet(ViewSet, BaseView, Error):
    """
    继承ViewSet，
    Response：自定义返回格式
    Error: 自定义错误信息
    """
    pass


class ModelBaseViewSet(ModelViewSet, BaseView, Error):
    """
    继承ModelViewSet，
    Response：自定义返回格式
    Error: 自定义错误信息
    """
    pass


