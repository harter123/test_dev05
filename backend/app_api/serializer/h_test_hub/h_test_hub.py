from rest_framework import serializers
from app_api.models.h_test_hub.h_test_hub_model import HTestHub


# 只是用来做序列化
class HTestHubViewSerializer(serializers.ModelSerializer):
    creator_name = serializers.CharField(source="creator.username")  # 反向获取用户的名称
    create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')  # 日期格式化

    class Meta:
        model = HTestHub
        fields = ['id', 'name', 'flag', 'describe', 'creator_id', "creator_name", 'create_time', 'h_test_plan_num']  # 要显示的字段
        # fields = "__all__"


# 用来做参数检验，以及数据保存
class HTestHubValidator(serializers.Serializer):
    """
    测试库的验证器
    """
    name = serializers.CharField(required=True, max_length=50,
                                 error_messages={"required": "name不能为空",
                                                 "invalid": "类型不对",
                                                 "max_length": "长度不能大于50"})
    flag = serializers.CharField(required=True, max_length=50,
                                 error_messages={"required": "flag不能为空",
                                                 "invalid": "类型不对",
                                                 "max_length": "长度不能大于20"})
    create_id = serializers.IntegerField(required=True)
    describe = serializers.CharField(required=False)
    h_test_plan_num = serializers.IntegerField(required=False)

    def create(self, validated_data):
        """
        创建
        """
        test_hub = HTestHub.objects.create(**validated_data)
        return test_hub

    def update(self, instance, validated_data):
        """
        更新
        instance - 更新的对象 - 从数据库里查出来的
        validated_data - 更新的数据
        """
        instance.name = validated_data.get("name", instance.name)
        instance.describe = validated_data.get("describe", instance.describe)
        instance.h_test_plan_num = validated_data.get("h_test_plan_num", instance.h_test_plan_num)
        instance.flag = validated_data.get("flag", instance.flag)
        instance.creator_id = validated_data.get("creator_id", instance.creator_id)
        instance.save()
        return instance



















