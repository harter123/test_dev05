import traceback
from django.utils.deprecation import MiddlewareMixin

from app_common.utils.response import Error, response_success


class CommonException(MiddlewareMixin):

    def process_exception(self, request, exception):
        traceback.print_exc()
        return response_success(False, error=Error.SYS_ERROR, data=str(exception), json_flag=True)
