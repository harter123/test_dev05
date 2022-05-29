from app_api.models.h_test_hub.h_test_plan_model import HTestPlan, HTestPlanRelateTestCase
from app_api.serializer.h_test_hub.h_test_plan import HTestPlanValidator, HTestPlanViewSerializer, \
    HTestPlanUpdateValidator, HTestPlanTestCaseViewSerializer, HTestPlanTestCaseUpdateValidator, \
    HTestPlanTestCaseCreateValidator
from app_api.views.h_test_hub.h_test_case_module_view import make_module_tree
from app_api.views.h_test_hub.h_test_case_view import get_target_from_tree, get_all_module_children_ids
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
        name = request.query_params.get("keyword", "")
        status_id = request.query_params.get("statusId", 0)
        test_hub_id = request.query_params.get("hTestHubId", 0)  #

        status_id = int(status_id)
        test_hub_id = int(test_hub_id)

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
        ret = ser.data
        all_num = ret['success_num'] + ret['failed_num'] + ret['skip_num'] + ret['block_num'] + ret["not_start_num"]
        run_num = ret['success_num'] + ret['failed_num'] + ret['block_num']
        if all_num == 0:  # 分母不能是0，所以需要做异常处理
            ret["runRate"] = 0
        else:
            ret["runRate"] = (run_num * 100) / all_num
            ret["runRate"] = round(ret["runRate"], 1)

        if run_num == 0:
            ret["successRate"] = 0
        else:
            ret["successRate"] = (ret['success_num'] * 100) / run_num
            ret["successRate"] = round(ret["successRate"], 1)
        return self.response_success(data=ret)


class HTestPlanTestCaseViewSet(ModelBaseViewSet):
    serializer_class = HTestPlanTestCaseViewSerializer
    queryset = HTestPlanRelateTestCase.objects.all()

    def update_statistics(self, test_plan_id):
        """
    {"id": 1, 'name': "未开始", "type": "info"},
    {"id": 2, 'name': "阻塞", "type": "warning"},
    {"id": 3, 'name': "通过", "type": "success"},
    {"id": 4, 'name': "跳过", "type": "info"},
    {"id": 5, 'name': "失败", "type": "danger"}
        """
        success_num = HTestPlanRelateTestCase.objects.filter(run_status_id=3, h_test_plan_id=test_plan_id).count()
        failed_num = HTestPlanRelateTestCase.objects.filter(run_status_id=5, h_test_plan_id=test_plan_id).count()
        skip_num = HTestPlanRelateTestCase.objects.filter(run_status_id=4, h_test_plan_id=test_plan_id).count()
        block_num = HTestPlanRelateTestCase.objects.filter(run_status_id=2, h_test_plan_id=test_plan_id).count()
        not_start_num = HTestPlanRelateTestCase.objects.filter(run_status_id=1, h_test_plan_id=test_plan_id).count()
        HTestPlan.objects.filter(id=test_plan_id).update(success_num=success_num,
                                                         failed_num=failed_num,
                                                         skip_num=skip_num,
                                                         block_num=block_num,
                                                         not_start_num=not_start_num)

    def list(self, request, *args, **kwargs):
        """
        get - v1/TestPlan/TestCase 获取测试计划下的测试用例列表
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        page = request.query_params.get("page", "1")
        size = request.query_params.get("size", "5")
        module_id = request.query_params.get("hModuleId", 0)
        test_plan_id = request.query_params.get("hTestPlanId", 0)
        test_hub_id = request.query_params.get("hTestHubId", 0)
        module_id = int(module_id)
        test_plan_id = int(test_plan_id)
        test_hub_id = int(test_hub_id)

        if not test_plan_id:
            return self.response_success(success=False, error=self.TESTPLAN_ID_NULL)
        if not test_hub_id:
            return self.response_success(success=False, error=self.TESTHUB_ID_NULL)

        if not module_id:
            test_plan_test_case = HTestPlanRelateTestCase.objects.filter(h_test_plan_id=test_plan_id)
        else:

            module_tree = make_module_tree(test_hub_id)
            target = get_target_from_tree(int(module_id), module_tree)
            if not target:
                return self.response_success(data=[])

            module_ids = [module_id]
            get_all_module_children_ids(target, module_ids)

            test_plan_test_case = HTestPlanRelateTestCase.objects.filter(h_test_plan_id=test_plan_id,
                                                                         h_test_case__h_test_module_id__in=module_ids,
                                                                         h_test_case__is_delete=False)
        pg = Pagination()
        page_data = pg.paginate_queryset(queryset=test_plan_test_case, request=request, view=self)
        ser = HTestPlanTestCaseViewSerializer(instance=page_data, many=True)
        data = {
            "total": len(test_plan_test_case),
            "page": int(page),
            "size": int(size),
            "testCaseList": ser.data
        }
        return self.response_success(data=data)

    def destroy(self, request, pk, *args, **kwargs):
        """
        delete - v1/TestPlan/testcase/<pk> 移除关联关系，这个id是关联表的id
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        # 删除关联表的数据
        HTestPlanRelateTestCase.objects.filter(id=pk).delete()
        return self.response_success(data={})

    def update(self, request, pk, *args, **kwargs):
        """
        put - v1/TestPlan/testcase/<pk>/  修改执行状态
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        # 判断关联表数据是否存在
        test_plan_case = HTestPlanRelateTestCase.objects.filter(id=pk).first()
        if not test_plan_case:
            return self.response_success(success=False, error=self.TESTPLANTESTCASE_ID_NULL)

        # 获取前端传来的参数
        params = request.data

        # 更新测试库数据000
        serializer = HTestPlanTestCaseUpdateValidator(instance=test_plan_case, data=params)
        serializer.is_valid(raise_exception=True)  # 规则校验
        serializer.save()  # 把数据保存到数据库

        self.update_statistics(test_plan_case.h_test_plan_id)

        return self.response_success()

    def create(self, request, *args, **kwargs):
        """
        post - v1/TestPlan/testcase  创建测试计划和测试用例的关联
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        # 数据创建
        params = request.data

        serializer = HTestPlanTestCaseCreateValidator(data=params)
        serializer.is_valid(raise_exception=True)  # 规则校验

        test_plan_id = params.get('test_plan_id')
        test_case_ids = params.get('test_case_ids')
        for t_id in test_case_ids:
            # if HTestPlanRelateTestCase.objects.filter(h_test_plan_id=test_plan_id, h_test_case_id=t_id):
            #     continue
            # HTestPlanRelateTestCase.objects.create(h_test_plan_id=test_plan_id, h_test_case_id=t_id)
            HTestPlanRelateTestCase.objects.get_or_create(h_test_plan_id=test_plan_id, h_test_case_id=t_id)

        # 数据的序列化，返回给前端
        return self.response_success()


class HToDoTestPlanViewSet(ModelBaseViewSet):
    serializer_class = HTestPlanTestCaseViewSerializer
    queryset = HTestPlanRelateTestCase.objects.all()

    def list(self, request, *args, **kwargs):
        """
        get - v1/todo/TestPlan/ 获取测试用例列表
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        page = request.query_params.get("page", "1")
        size = request.query_params.get("size", "5")
        name = request.query_params.get("keyword", "")
        status_id = request.query_params.get("statusId", 0)

        status_id = int(status_id)

        user = self.get_user(request)

        query = {
            "owner_id": user.id
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
