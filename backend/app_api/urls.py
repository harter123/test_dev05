from django.urls import path
from rest_framework import routers

from app_api.views.h_test_hub.h_test_hub_recent_visited_view import HTestHubRecentVisitedViewSet
from app_api.views.h_test_hub.h_test_plan_view import HTestPlanViewSet, HTestPlanTestCaseViewSet, HToDoTestPlanViewSet
from app_api.views.user_views import LoginView, UsersView
from app_api.views.register_views import RegisterView
from app_api.views.project_view import ProjectView, ProjectModuleView
from app_api.views.module_view import ModuleView
from app_api.views.module_view import ModuleTreeView
from app_api.views.case_view import CaseViewSet
from app_api.views.task_view import TaskViewSet
from app_api.views.result_view import ResultViewSet
from app_api.views.h_test_hub.h_test_hub_view import HTestHubViewSet
from app_api.views.h_test_hub.h_test_case_module_view import HTestCaseModuleViewSet
from app_api.views.h_test_hub.h_test_case_view import HTestCaseViewSet

url_path = [
    path('v1/users/', UsersView.as_view()),
    path('v1/login/', LoginView.as_view()),
    path('v1/register/', RegisterView.as_view()),
    path('v1/project/', ProjectView.as_view()),
    path('v1/project/<int:pk>/', ProjectView.as_view()),
    path("v1/project/<int:pk>/module/", ProjectModuleView.as_view()),

    path('v1/module/', ModuleView.as_view()),
    path('v1/module/<int:pk>/', ModuleView.as_view()),
    path("v1/module/tree/", ModuleTreeView.as_view()),
]

router = routers.SimpleRouter()
router.register(r'v1/case', CaseViewSet)  # 用例管理
router.register(r'v1/task', TaskViewSet)  # 任务管理
router.register(r'v1/result', ResultViewSet)  # 结果管理
router.register(r'v1/testmodule', HTestCaseModuleViewSet)  # 测试库模块管理
router.register(r'v1/testhub', HTestHubViewSet)  # 测试库管理
router.register(r'v1/testcase', HTestCaseViewSet)  # 测试用例管理
router.register(r'v1/testplan/testcase', HTestPlanTestCaseViewSet)  # 测试计划用例管理
router.register(r'v1/testplan', HTestPlanViewSet)  # 测试计划管理
router.register(r'v1/todo/testplan', HToDoTestPlanViewSet)  # 测试计划管理
router.register(r'v1/recent/testhub', HTestHubRecentVisitedViewSet, basename="recent")  # 测试库管理

urlpatterns = url_path + router.urls
