import datetime
from rest_framework import serializers
from app_api.models.h_test_hub.h_test_case_model import HTestCase


# 只是用来做序列化
class HTestCaseViewSerializer(serializers.ModelSerializer):
    creator_name = serializers.CharField(source="creator.username")  # 反向获取用户的名称
    create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')  # 日期格式化

    class Meta:
        model = HTestCase
        fields = ['id', 'title', 'pre_step', 'step', 'post_step', "expect", 'create_time', 'creator_name',
                  'status_id', 'priority_id', 'type_id', 'h_test_hub_id', 'h_test_module_id']  # 要显示的字段


# 用来做参数检验，以及数据创建
class HTestCaseValidator(serializers.Serializer):
    """
    测试库的验证器
    """
    creator_id = serializers.IntegerField(required=True)
    h_test_hub_id = serializers.IntegerField(required=True)
    h_test_module_id = serializers.IntegerField(required=True)
    title = serializers.CharField(required=True, max_length=50,
                                  error_messages={"required": "title不能为空",
                                                  "invalid": "类型不对",
                                                  "max_length": "长度不能大于300"})

    pre_step = serializers.CharField(required=False, allow_blank=True, )
    step = serializers.CharField(required=False, allow_blank=True, )
    post_step = serializers.CharField(required=False, allow_blank=True, )
    expect = serializers.CharField(required=False, allow_blank=True, )

    status_id = serializers.IntegerField(required=False)
    priority_id = serializers.IntegerField(required=False)
    type_id = serializers.IntegerField(required=False)

    def create(self, validated_data):
        """
        创建
        validated_data 经过校验的字典数据
        """
        # ** 等于是把字典平铺开来，例如 a = {"a1"：1，”b1“: 2},平铺开来九食 a1=1,b1=2
        test_hub = HTestCase.objects.create(**validated_data)
        return test_hub

    def update(self, instance, validated_data):
        return instance


# 用来做参数检验，以及数据编辑
class HTestCaseUpdateValidator(HTestCaseValidator):
    """
    测试库的验证器
    """
    creator_id = serializers.IntegerField(required=False)
    h_test_hub_id = serializers.IntegerField(required=False)
    h_test_module_id = serializers.IntegerField(required=False)
    title = serializers.CharField(required=False, max_length=50,
                                  error_messages={"required": "title不能为空",
                                                  "invalid": "类型不对",
                                                  "max_length": "长度不能大于300"})

    pre_step = serializers.CharField(required=False, allow_blank=True, )
    step = serializers.CharField(required=False, allow_blank=True, )
    post_step = serializers.CharField(required=False, allow_blank=True, )
    expect = serializers.CharField(required=False, allow_blank=True, )

    status_id = serializers.IntegerField(required=False)
    priority_id = serializers.IntegerField(required=False)
    type_id = serializers.IntegerField(required=False)

    def create(self, validated_data):
        return None

    def update(self, instance, validated_data):
        """
        更新
        instance - 更新的对象 - 从数据库里查出来的
        validated_data - 更新的数据
        """
        instance.h_test_hub_id = validated_data.get("h_test_hub_id", instance.h_test_hub)
        instance.h_test_module_id = validated_data.get("h_test_module_id", instance.h_test_module_id)
        instance.title = validated_data.get("title", instance.title)
        instance.pre_step = validated_data.get("pre_step", instance.pre_step)
        instance.step = validated_data.get("step", instance.step)
        instance.post_step = validated_data.get("post_step", instance.post_step)
        instance.expect = validated_data.get("expect", instance.expect)
        instance.status_id = validated_data.get("status_id", instance.status_id)
        instance.priority_id = validated_data.get("priority_id", instance.priority_id)
        instance.type_id = validated_data.get("type_id", instance.type_id)
        if not instance.update_time:
            instance.update_time = datetime.datetime.now()
        if not instance.create_time:
            instance.create_time = datetime.datetime.now()
        instance.save()
        return instance
