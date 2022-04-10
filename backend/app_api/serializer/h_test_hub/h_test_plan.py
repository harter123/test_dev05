import datetime
from rest_framework import serializers
# 只是用来做序列化
from app_api.models.h_test_hub.h_test_plan_model import HTestPlan


class HTestPlanViewSerializer(serializers.ModelSerializer):
    creator_name = serializers.CharField(source="creator.username")  # 反向获取用户的名称
    owner_name = serializers.CharField(source="owner.username")  # 反向获取用户的名称
    create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')  # 日期格式化
    start_date = serializers.DateField(format='%Y-%m-%d')  # 日期格式化
    end_date = serializers.DateField(format='%Y-%m-%d')  # 日期格式化

    class Meta:
        model = HTestPlan
        fields = ['id', 'name', 'h_test_hub_id', 'status_id', 'start_date', 'end_date', "owner_id", 'creator_id',
                  "owner_name", 'create_time', 'creator_name', ]  # 要显示的字段


# 用来做参数检验，以及数据创建
class HTestPlanValidator(serializers.Serializer):
    """
    测试库的验证器
    """
    status_id = serializers.IntegerField(required=False)

    creator_id = serializers.IntegerField(required=True)
    owner_id = serializers.IntegerField(required=True)
    h_test_hub_id = serializers.IntegerField(required=True)
    name = serializers.CharField(required=True, max_length=300,
                                 error_messages={"required": "name不能为空",
                                                 "invalid": "类型不对",
                                                 "max_length": "长度不能大于300"})

    start_date = serializers.DateField(required=True, format="%Y-%m-%d")
    end_date = serializers.DateField(required=True, format="%Y-%m-%d")

    def create(self, validated_data):
        """
        创建
        validated_data 经过校验的字典数据
        """
        # ** 等于是把字典平铺开来，例如 a = {"a1"：1，”b1“: 2},平铺开来九食 a1=1,b1=2
        test_hub = HTestPlan.objects.create(**validated_data)
        return test_hub

    def update(self, instance, validated_data):
        return instance


# 用来做参数检验，以及数据编辑
class HTestPlanUpdateValidator(HTestPlanValidator):
    """
    测试库的验证器
    """
    status_id = serializers.IntegerField(required=False)
    creator_id = serializers.IntegerField(required=False)
    owner_id = serializers.IntegerField(required=False)
    h_test_hub_id = serializers.IntegerField(required=False)
    name = serializers.CharField(required=False, max_length=300,
                                 error_messages={"required": "name不能为空",
                                                 "invalid": "类型不对",
                                                 "max_length": "长度不能大于300"})

    start_date = serializers.DateField(required=False, format="%Y-%m-%d")
    end_date = serializers.DateField(required=False, format="%Y-%m-%d")

    def create(self, validated_data):
        return None

    def update(self, instance, validated_data):
        """
        更新
        instance - 更新的对象 - 从数据库里查出来的
        validated_data - 更新的数据
        """
        instance.h_test_hub_id = validated_data.get("h_test_hub_id", instance.h_test_hub_id)
        instance.status_id = validated_data.get("status_id", instance.status_id)
        instance.name = validated_data.get("name", instance.name)
        instance.owner_id = validated_data.get("owner_id", instance.owner_id)
        instance.start_date = validated_data.get("start_date", instance.start_date)
        instance.end_date = validated_data.get("end_date", instance.end_date)

        if not instance.update_time:
            instance.update_time = datetime.datetime.now()
        if not instance.create_time:
            instance.create_time = datetime.datetime.now()
        instance.save()
        return instance