
from app_api.models.h_test_hub.h_test_hub_model import HTestHub
from app_api.serializer.h_test_hub.h_test_hub import HTestHubValidator, HTestHubViewSerializer
from app_common.utils.pagination import Pagination
from app_common.utils.base_view import ModelBaseViewSet


class HTestHubViewSet(ModelBaseViewSet):
    serializer_class = HTestHubViewSerializer

    def create(self, request, *args, **kwargs):
        """
        post - v1/testhub  创建测试库
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        # 数据创建
        params = request.data
        user = self.get_user(request)
        params["creator_id"] = user.id
        params["h_test_plan_num"] = 0

        serializer = HTestHubValidator(data=params)
        serializer.is_valid(raise_exception=True) # 规则校验
        test_hub = serializer.save()  # 把数据保存到数据库

        # 数据的序列化，返回给前端
        ser = HTestHubViewSerializer(test_hub)
        return self.response_success(data=ser.data)

    def update(self, request, pk, *args, **kwargs):
        """
        put - v1/testhub/<pk>/  编辑测试库
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        # 判断测试库是否存在
        test_hub = HTestHub.objects.filter(id=pk).first()
        if not test_hub:
            return self.response_success(success=False, error=self.TESTHUB_ID_NULL)

        # 获取前端传来的参数
        params = request.data

        # 更新测试库数据
        serializer = HTestHubValidator(instance=test_hub, data=params)
        serializer.is_valid(raise_exception=True)  # 规则校验
        test_hub = serializer.save()  # 把数据保存到数据库

        # 数据的序列化，返回给前端
        ser = HTestHubViewSerializer(test_hub)
        return self.response_success(data=ser.data)

    def list(self, request, *args, **kwargs):
        """
        get - v1/testhub/ 获取测试库列表
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        page = request.query_params.get("page", "1")
        size = request.query_params.get("size", "5")
        keyword = request.query_params.get("keyword", "")
        if not keyword:
            test_hubs = HTestHub.objects.filter(is_delete=False)
        else:
            test_hubs = HTestHub.objects.filter(is_delete=False, name__contains=keyword)

        pg = Pagination()
        page_data = pg.paginate_queryset(queryset=test_hubs, request=request, view=self)
        ser = HTestHubViewSerializer(instance=page_data, many=True)
        data = {
            "total": len(test_hubs),
            "page": int(page),
            "size": int(size),
            "testHubList": ser.data
        }
        return self.response_success(data=data)

    def destroy(self, request, pk, *args, **kwargs):
        """
        delete - v1/testhub/<pk> 删除测试库
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        # 判断测试库是否存在
        test_hub = HTestHub.objects.filter(id=pk).first()
        if not test_hub:
            return self.response_success(success=False, error=self.TESTHUB_ID_NULL)
        test_hub.is_delete = True
        test_hub.save()
        return self.response_success(data={})

    def retrieve(self, request, pk, *args, **kwargs):
        """
        get - v1/testhub/<pk> 获取单个测试库
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        # 判断测试库是否存在
        test_hub = HTestHub.objects.filter(id=pk).first()
        if not test_hub:
            return self.response_success(success=False, error=self.TESTHUB_ID_NULL)

        # 数据的序列化，返回给前端
        ser = HTestHubViewSerializer(test_hub)
        return self.response_success(data=ser.data)













