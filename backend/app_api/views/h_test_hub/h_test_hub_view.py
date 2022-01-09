from app_api.models import Module
from app_api.models.h_test_hub.h_test_hub_model import HTestHub
from app_api.serializer.h_test_hub.h_test_hub import HTestHubValidator, HTestHubViewSerializer
from app_api.serializer.module import ModuleValidator, ModuleSerializer
from app_common.utils.pagination import Pagination
from app_common.utils.base_view import BaseAPIView, ModelBaseViewSet


class HTestHubViewSet(ModelBaseViewSet):

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
        user = request.user
        params["creator_id"] = user.id

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
            return self.response_success(error=self.TESTHUB_ID_NULL)

        # 获取前端传来的参数
        params = request.data

        # 序列化旧的测试库数据
        ser = HTestHubViewSerializer(test_hub)
        test_hub_data = ser.data

        # 把前端传来的数据update进去
        test_hub_data.update(params)

        # 更新测试库数据
        serializer = HTestHubValidator(instance=test_hub, data=test_hub_data)
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
        pass

    def destroy(self, request, *args, **kwargs):
        """
        delete - v1/testhub/<pk> 删除测试库
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        pass

    def retrieve(self, request, *args, **kwargs):
        """
        get - v1/testhub/<pk> 获取单个测试库
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        pass















