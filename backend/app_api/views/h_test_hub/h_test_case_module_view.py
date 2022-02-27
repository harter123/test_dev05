
from app_api.models.h_test_hub.h_module_model import HTestCaseModule
from app_api.serializer.h_test_hub.h_test_case_module import HTestCaseModuleValidator, HTestCaseModuleViewSerializer
from app_common.utils.pagination import Pagination
from app_common.utils.base_view import ModelBaseViewSet


def sort_module(target, data):
    if 0 == len(data) or not target:
        return

    children_index_list = []

    # 找出全部子节点的index
    for i, v in enumerate(data):
        if v['parent_id'] == target['id']:
            children_index_list.append(i)

    # 遍历全部的index
    for index in children_index_list:
        v = data.pop(index) # 返回并且删除数组的数据

        if "children" not in target:
            target["children"] = []

        target['children'].append(v)


class HTestCaseModuleViewSet(ModelBaseViewSet):
    serializer_class = HTestCaseModuleViewSerializer

    def create(self, request, *args, **kwargs):
        """
        post - v1/testhub/testcase/module  创建测试库的用例模块
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        # 数据创建
        params = request.data
        serializer = HTestCaseModuleValidator(data=params)
        serializer.is_valid(raise_exception=True) # 规则校验
        test_module = serializer.save()  # 把数据保存到数据库
        # 数据的序列化，返回给前端
        ser = HTestHubViewSerializer(test_module)
        return self.response_success(data=ser.data)

    def update(self, request, pk, *args, **kwargs):
        """
        put - v1/testhub/testcasemodule/<pk>/  编辑测试库
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        # 判断测试模块是否存在
        test_case_module = HTestCaseModule.objects.filter(id=pk).first()
        if not test_case_module:
            return self.response_success(success=False, error=self.TESTCASEMODULE_ID_NULL)

        # 获取前端传来的参数
        params = request.data

        # 更新测试库数据
        serializer = HTestCaseModuleValidator(instance=test_case_module, data=params)
        serializer.is_valid(raise_exception=True)  # 规则校验
        test_case_module = serializer.save()  # 把数据保存到数据库

        # 数据的序列化，返回给前端
        ser = HTestCaseModuleViewSerializer(test_case_module)
        return self.response_success(data=ser.data)

    def list(self, request, *args, **kwargs):
        """
        get - v1/testhub/testcasemodule/ 获取测试库模块列表
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        test_hub_id = request.query_params.get("testHubId", 0)
        if not test_hub_id:
            return self.response_success(success=False, error=self.ParamsTypeError)

        # 以分类数据
        sorted_list = HTestCaseModule.objects.filter(h_test_hub_id=test_hub_id, is_delete=False, parent_id=0)
        e_list = HTestCaseModule.objects.filter(h_test_hub_id=test_hub_id, is_delete=False, parent_id__gt=0) # 未分类数据

        sorted_list_dict = HTestCaseModuleViewSerializer(sorted_list, many=True).data
        e_list_dict = HTestCaseModuleViewSerializer(e_list, many=True).data

        for item in sorted_list_dict:
            if 0 == len(e_list_dict) or not item:
                continue
            sort_module(item, e_list_dict) # 完成了第一层的遍历处理
            children = item.get('children', []) # 拿第二层的数据
            if 0 == len(children):
                continue

            for c_item in children:   # 处理第二层的遍历数据
                if 0 == len(e_list_dict):
                    continue
                sort_module(c_item, e_list_dict)

        return self.response_success(data=sorted_list_dict)

    def destroy(self, request, pk, *args, **kwargs):
        """
        delete - v1/testhub/testcasemodule/<pk> 删除测试库
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        # 判断测试库是否存在
        test_case_module = HTestCaseModule.objects.filter(id=pk).first()
        if not test_case_module:
            return self.response_success(success=False, error=self.TESTCASEMODULE_ID_NULL)
        test_case_module.is_delete = True
        test_case_module.save()
        return self.response_success(data={})

    def retrieve(self, request, pk, *args, **kwargs):
        """
        get - v1/testhub/testcasemodule/<pk> 获取单个测试库
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        # 判断测试库是否存在
        test_case_module = HTestCaseModule.objects.filter(id=pk).first()
        if not test_case_module:
            return self.response_success(success=False, error=self.TESTHUB_ID_NULL)

        # 数据的序列化，返回给前端
        ser = HTestCaseModuleViewSerializer(test_case_module)
        return self.response_success(data=ser.data)













