
from app_api.models.h_test_hub.h_test_hub_visited_recently_model import HTestHubVisitedRecently
from app_api.serializer.h_test_hub.h_test_hub_visited_recent import HTestHubVisitedRecentViewSerializer, \
    HTestHubVisitedRecentValidator
from app_common.utils.base_view import ModelBaseViewSet


class HTestHubRecentVisitedViewSet(ModelBaseViewSet):
    serializer_class = HTestHubVisitedRecentViewSerializer
    queryset = HTestHubVisitedRecently.objects.all()

    def create(self, request, *args, **kwargs):
        """
        post - v1/recent/testhub/ 创建最近访问的测试库
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        # 数据创建
        params = request.data
        user = self.get_user(request)
        params["user_id"] = user.id

        print(123)
        serializer = HTestHubVisitedRecentValidator(data=params)
        serializer.is_valid(raise_exception=True) # 规则校验
        serializer.save()  # 把数据保存到数据库

        # 数据的序列化，返回给前端
        return self.response_success()

    def list(self, request, *args, **kwargs):
        """
        get - v1/recent/testhub/ 获取最近访问的测试库列表
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        user = self.get_user(request)
        test_hubs = HTestHubVisitedRecently.objects.filter(user_id=user.id, is_delete=False).order_by('-update_time')
        ser = HTestHubVisitedRecentViewSerializer(instance=test_hubs[:5], many=True)
        return self.response_success(data=ser.data)













