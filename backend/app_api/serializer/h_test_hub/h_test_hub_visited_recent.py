from datetime import datetime

from rest_framework import serializers

from app_api.models.h_test_hub.h_test_hub_model import HTestHub
from app_api.models.h_test_hub.h_test_hub_visited_recently_model import HTestHubVisitedRecently


# 只是用来做序列化
class HTestHubVisitedRecentViewSerializer(serializers.ModelSerializer):
    test_hub_name = serializers.CharField(source="h_test_hub.name")  # 反向获取用户的名称
    test_hub_creator_name = serializers.CharField(source="h_test_hub.creator.username")
    test_hub_create_time = serializers.DateTimeField(source="h_test_hub.create_time", format='%Y-%m-%d')

    class Meta:
        model = HTestHubVisitedRecently
        fields = ['test_hub_name', 'h_test_hub_id', 'test_hub_creator_name', 'test_hub_create_time']  # 要显示的字段
        # fields = "__all__"

# 用来做参数检验，以及数据保存
class HTestHubVisitedRecentValidator(serializers.Serializer):
    """
    测试库的验证器
    """
    user_id = serializers.IntegerField(required=True)
    h_test_hub_id = serializers.IntegerField(required=True)

    def create(self, validated_data):
        """
        创建
        validated_data 经过校验的字典数据
        {
        "user_id": 1,
        "h_test_hub_id": 2,
        }
        """
        # ** 等于是把字典平铺开来，例如 a = {"a1"：1，”b1“: 2},平铺开来九食 a1=1,b1=2
        user_id = validated_data.get('user_id', 0)
        h_test_hub_id = validated_data.get('h_test_hub_id', 0)

        # 如果数据存在，则更新update时间，不存在，就插入数据
        test_hub_visited = HTestHubVisitedRecently.objects.filter(user_id=user_id, h_test_hub_id=h_test_hub_id).first()
        if test_hub_visited:
            test_hub_visited.update_time = datetime.now()
            test_hub_visited.save()
        else:
            test_hub_visited = HTestHubVisitedRecently.objects.create(**validated_data)

        return test_hub_visited

    def update(self, instance, validated_data):
        """
        更新
        instance - 更新的对象 - 从数据库里查出来的
        validated_data - 更新的数据
        """
        instance.user_id = validated_data.get("user_id", instance.name)
        instance.h_test_hub_id = validated_data.get("h_test_hub_id", instance.h_test_hub_id)
        instance.save()
        return instance
