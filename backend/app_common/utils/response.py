from rest_framework.response import Response
from django.http.response import JsonResponse


class Error:
    """
    子定义错误码与错误信息
    """
    USER_OR_PAWD_NULL = {"10010": "用户名密码为空"}
    USER_OR_PAWD_ERROR = {"10011": "用户名密码错误"}
    PAWD_ERROR = {"10012": "两次密码不一致"}

    ParamsTypeError = {"30020": "参数类型错误"}
    JSON_TYPE_ERROR = {"30030": "JSON格式错误"}
    SYS_ERROR = {"30040": "系统错误"}

    USER_ID_NULL = {"40010": "用户id不存在"}

    PROJECT_ID_NULL = {"10020": "项目id不存在"}
    PROJECT_OBJECT_NULL = {"10021": "通过id查询项目不存在"}
    PROJECT_DELETE_ERROR = {"10023": "项目删除失败"}

    MODULE_ID_NULL = {"10030": "模块id不存在"}
    MODULE_OBJECT_NULL = {"10031": "模块对象不存在"}
    MODULE_DELETE_ERROR = {"10032": "模块删除失败"}

    CASE_ID_NULL = {"10040": "用例id不存在"}
    CASE_OBJECT_NULL = {"10041": "通过id查询用例不存在"}
    CASE_HEADER_ERROR = {"10042": "header类型错误，不是json"}
    CASE_PARAMS_BODY_ERROR = {"10043": "params_body类型错误，不是json"}
    ASSERT_INCLUDE_FAIL = {"10044": "断言包含失败"}
    ASSERT_EQUAL_FAIL = {"10045": "断言相等失败"}

    TASK_ID_NULL = {"10051", "task ID不存在"}
    TASK_OBJECT_NULL = {"10041": "通过id查询任务不存在"}

    RESULT_ID_NULL = {"10061", "task ID不存在"}
    RESULT_OBJECT_NULL = {"10061": "通过id查询任务不存在"}

    TESTHUB_ID_NULL = {"10070": "测试库id不存在"}
    TESTHUB_OBJECT_NULL = {"10071": "测试库对象不存在"}
    TESTHUB_DELETE_ERROR = {"10072": "测试库删除失败"}

    TESTCASEMODULE_ID_NULL = {"10080": "测试库模块id不存在"}
    TESTCASEMODULE_OBJECT_NULL = {"10081": "测试库模块对象不存在"}
    TESTCASEMODULE_DELETE_ERROR = {"10082": "测试库模块删除失败"}

    TESTCASE_ID_NULL = {"10090": "测试用例id不存在"}
    TESTCASE_OBJECT_NULL = {"10091": "测试用例对象不存在"}
    TESTCASE_DELETE_ERROR = {"10092": "测试用例删除失败"}

    TESTPLAN_ID_NULL = {"10100": "测试计划id不存在"}
    TESTPLAN_OBJECT_NULL = {"10101": "测试计划对象不存在"}
    TESTPLAN_DELETE_ERROR = {"10192": "测试计划删除失败"}

    TESTPLANTESTCASE_ID_NULL = {"10200": "测试计划用例关联id不存在"}
    TESTPLANESTCASE_OBJECT_NULL = {"10201": "测试计划用例关联对象不存在"}
    TESTPLANESTCASE_DELETE_ERROR = {"10292": "测试计划用例关联删除失败"}

def response_fail(error=""):
    """
    返回失败, 主要用于参数验证失败
    """
    error_msg = {
        "30010": str(error)
    }
    return response_success(success=False, error=error_msg, result=[])


def response_success(success: bool = True, error={}, data: any = [], json_flag=False) -> Response:
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
        "error": {
            "code": error_code,
            "message": error_msg
        },
        "data": data
    }
    if json_flag:
        return JsonResponse(resp)
    else:
        return Response(resp)
