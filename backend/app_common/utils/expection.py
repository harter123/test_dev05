import traceback
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    traceback.print_exc()
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if response is not None:
        response.data['status_code'] = response.status_code
        # response.data['message'] =response.data['detail']    #增加message这个key
        # response.data['message'] ='方法不对'    #增加message这个key
    return response
