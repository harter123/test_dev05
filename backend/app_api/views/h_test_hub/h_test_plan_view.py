from app_api.models.h_test_hub.h_test_plan_model import HTestPlan
from app_api.serializer.h_test_hub.h_test_plan import HTestPlanValidator, HTestPlanViewSerializer, \
    HTestPlanUpdateValidator
from app_common.utils.pagination import Pagination
from app_common.utils.base_view import ModelBaseViewSet


class HTestPlanViewSet(ModelBaseViewSet):
    serializer_class = HTestPlanViewSerializer
    queryset = HTestPlan.objects.all()

    def create(self, request, *args, **kwargs):
        """
        post - v1/TestPlan  创建测试计划
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        # 数据创建
        params = request.data
        user = self.get_user(request)
        params["creator_id"] = user.id

        serializer = HTestPlanValidator(data=params)
        serializer.is_valid(raise_exception=True)  # 规则校验
        test_plan = serializer.save()  # 把数据保存到数据库

        # 数据的序列化，返回给前端
        ser = HTestPlanViewSerializer(test_plan)
        return self.response_success(data=ser.data)

    def update(self, request, pk, *args, **kwargs):
        """
        put - v1/TestPlan/<pk>/  编辑测试用例
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        # 判断测试库是否存在
        test_plan = HTestPlan.objects.filter(id=pk).first()
        if not test_plan:
            return self.response_success(success=False, error=self.TESTPLAN_ID_NULL)

        # 获取前端传来的参数
        params = request.data

        # 更新测试库数据
        serializer = HTestPlanUpdateValidator(instance=test_plan, data=params)
        serializer.is_valid(raise_exception=True)  # 规则校验
        serializer.save()  # 把数据保存到数据库

        # 数据的序列化，返回给前端
        test_plan = HTestPlan.objects.filter(id=pk).first()
        ser = HTestPlanViewSerializer(test_plan)
        return self.response_success(data=ser.data)

    def list(self, request, *args, **kwargs):
        """
        get - v1/TestPlan/ 获取测试用例列表
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        page = request.query_params.get("page", "1")
        size = request.query_params.get("size", "5")
        name = request.query_params.get("name", "")
        status_id = request.query_params.get("statusId", 0)
        test_hub_id = request.query_params.get("hTestHubId", 0)  #
        if not test_hub_id:
            return self.response_success(success=False, error=self.TESTHUB_ID_NULL)

        query = {
            "h_test_hub_id": test_hub_id
        }
        if name:
            query['name__contains'] = name
        if status_id:
            query['status_id'] = status_id

        # ** 等于是把字典平铺开来，例如 query = {"a1"：1，”b1“: 2},平铺开来九食 a1=1,b1=2
        test_plans = HTestPlan.objects.filter(is_delete=False, **query)
        pg = Pagination()
        page_data = pg.paginate_queryset(queryset=test_plans, request=request, view=self)
        ser = HTestPlanViewSerializer(instance=page_data, many=True)
        data = {
            "total": len(test_plans),
            "page": int(page),
            "size": int(size),
            "TestPlanList": ser.data
        }
        return self.response_success(data=data)

    def destroy(self, request, pk, *args, **kwargs):
        """
        delete - v1/TestPlan/<pk> 删除测试用例
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        # 判断测试库是否存在
        test_plan = HTestPlan.objects.filter(id=pk).first()
        if not test_plan:
            return self.response_success(success=False, error=self.TESTPLAN_ID_NULL)
        test_plan.is_delete = True
        test_plan.save()
        return self.response_success(data={})

    def retrieve(self, request, pk, *args, **kwargs):
        """
        get - v1/TestPlan/<pk> 获取单个测试用例
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        # 判断测试库是否存在
        test_plan = HTestPlan.objects.filter(id=pk).first()
        if not test_plan:
            return self.response_success(success=False, error=self.TESTPLAN_ID_NULL)

        # 数据的序列化，返回给前端
        ser = HTestPlanViewSerializer(test_plan)
        return self.response_success(data=ser.data)
