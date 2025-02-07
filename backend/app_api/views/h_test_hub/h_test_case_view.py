from app_api.models.h_test_hub.h_test_case_model import HTestCase
from app_api.serializer.h_test_hub.h_test_case import HTestCaseValidator, HTestCaseViewSerializer, \
    HTestCaseUpdateValidator
from app_api.views.h_test_hub.h_test_case_module_view import make_module_tree
from app_common.utils.pagination import Pagination
from app_common.utils.base_view import ModelBaseViewSet


def get_target_from_tree(module_id, module_tree):
    if not module_id or not module_tree:
        return None

    for item in module_tree:
        if item['id'] == module_id:
            return item

        return get_target_from_tree(module_id, item.get('children', None))


def get_all_module_children_ids(target, result):
    if not target:
        return

    for item in target.get('children', []):
        result.append(item['id'])
        get_all_module_children_ids(item.get('children', None), result)


class HTestCaseViewSet(ModelBaseViewSet):
    serializer_class = HTestCaseViewSerializer
    queryset = HTestCase.objects.all()

    def create(self, request, *args, **kwargs):
        """
        post - v1/testcase  创建测试用例
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        # 数据创建
        params = request.data
        user = self.get_user(request)
        params["creator_id"] = user.id

        serializer = HTestCaseValidator(data=params)
        serializer.is_valid(raise_exception=True)  # 规则校验
        test_case = serializer.save()  # 把数据保存到数据库

        # 数据的序列化，返回给前端
        ser = HTestCaseViewSerializer(test_case)
        return self.response_success(data=ser.data)

    def update(self, request, pk, *args, **kwargs):
        """
        put - v1/testcase/<pk>/  编辑测试用例
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        # 判断测试库是否存在
        test_case = HTestCase.objects.filter(id=pk).first()
        if not test_case:
            return self.response_success(success=False, error=self.TESTCASE_ID_NULL)

        # 获取前端传来的参数
        params = request.data

        # 更新测试库数据
        serializer = HTestCaseUpdateValidator(instance=test_case, data=params)
        serializer.is_valid(raise_exception=True)  # 规则校验
        serializer.save()  # 把数据保存到数据库

        # 数据的序列化，返回给前端
        test_case = HTestCase.objects.filter(id=pk).first()
        ser = HTestCaseViewSerializer(test_case)
        return self.response_success(data=ser.data)

    def list(self, request, *args, **kwargs):
        """
        get - v1/testcase/ 获取测试用例列表
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        page = request.query_params.get("page", "1")
        size = request.query_params.get("size", "5")
        module_ids_str = request.query_params.get("HModuleIds", "")  # id用逗号隔开： 1,2,3
        if not module_ids_str:
            module_ids_str = "all"
        module_id = module_ids_str
        test_hub_id = request.query_params.get("hTestHubId", 0)  #
        if not test_hub_id or not module_ids_str:
            self.response_success(data=[])

        if module_ids_str == "all":
            test_cases = HTestCase.objects.filter(is_delete=False, h_test_hub_id=test_hub_id)
        else:
            if not module_id:
                return self.response_success(data=[])

            module_tree = make_module_tree(test_hub_id)
            target = get_target_from_tree(int(module_id), module_tree)
            if not target:
                return self.response_success(data=[])

            module_ids = [module_id]
            get_all_module_children_ids(target, module_ids)

            test_cases = HTestCase.objects.filter(is_delete=False, h_test_hub_id=test_hub_id,
                                                  h_test_module_id__in=module_ids)

        pg = Pagination()
        page_data = pg.paginate_queryset(queryset=test_cases, request=request, view=self)
        ser = HTestCaseViewSerializer(instance=page_data, many=True)
        data = {
            "total": len(test_cases),
            "page": int(page),
            "size": int(size),
            "testCaseList": ser.data
        }
        return self.response_success(data=data)

    def destroy(self, request, pk, *args, **kwargs):
        """
        delete - v1/testcase/<pk> 删除测试用例
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        # 判断测试库是否存在
        test_case = HTestCase.objects.filter(id=pk).first()
        if not test_case:
            return self.response_success(success=False, error=self.TESTCASE_ID_NULL)
        test_case.is_delete = True
        test_case.save()
        return self.response_success(data={})

    def retrieve(self, request, pk, *args, **kwargs):
        """
        get - v1/testcase/<pk> 获取单个测试用例
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        # 判断测试库是否存在
        test_case = HTestCase.objects.filter(id=pk).first()
        if not test_case:
            return self.response_success(success=False, error=self.TESTCASE_ID_NULL)

        # 数据的序列化，返回给前端
        ser = HTestCaseViewSerializer(test_case)
        return self.response_success(data=ser.data)
