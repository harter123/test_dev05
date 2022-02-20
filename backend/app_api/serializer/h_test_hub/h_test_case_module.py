from rest_framework import serializers
from app_api.models.h_test_hub.h_module_model import HTestCaseModule


# 只是用来做序列化
class HTestCaseModuleViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = HTestCaseModule
        fields = ['id', 'name', 'h_test_hub_id', 'parent_id']  # 要显示的字段
        # fields = "__all__"


# 用来做参数检验，以及数据保存
class HTestCaseModuleValidator(serializers.Serializer):
    """
    测试库的验证器
    """
    name = serializers.CharField(required=True, max_length=50,
                                 error_messages={"required": "name不能为空",
                                                 "invalid": "类型不对",
                                                 "max_length": "长度不能大于50"})
    h_test_hub_id = serializers.IntegerField(required=True)
    parent_id = serializers.IntegerField(required=False)

    def create(self, validated_data):
        """
        创建
        validated_data 经过校验的字典数据
        {
        "name": "xxx",
        "h_test_hub_id": 1,
        "parent_id": 2
        }
        """
        # ** 等于是把字典平铺开来，例如 a = {"a1"：1，”b1“: 2},平铺开来九食 a1=1,b1=2
        test_hub = HTestHub.objects.create(**validated_data)
        return test_hub

    def update(self, instance, validated_data):
        """
        更新
        instance - 更新的对象 - 从数据库里查出来的
        validated_data - 更新的数据
        """
        instance.name = validated_data.get("name", instance.name)
        instance.h_test_hub_id = validated_data.get("h_test_hub_id", instance.h_test_hub_id)
        instance.parent_id = validated_data.get("parent_id", instance.parent_id)
        instance.save()
        return instance



















