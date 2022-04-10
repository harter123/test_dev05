from django.db import models
from django.contrib.auth.models import User

from app_api.models.h_test_hub.h_test_hub_model import HTestHub


class HTestPlan(models.Model):
    """
    测试计划表
    """
    name = models.CharField("名称", max_length=100, null=False, default="")
    status_id = models.IntegerField("状态", default=1)
    h_test_hub = models.ForeignKey(HTestHub, on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="creator")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner")
    start_date = models.DateField("开始日期", null=False)
    end_date = models.DateField("结束日期", null=False)
    is_delete = models.BooleanField("删除", default=False)
    update_time = models.DateTimeField("更新时间", auto_now=True)
    create_time = models.DateTimeField("创建时间", auto_now_add=True)

    def __str__(self):
        return self.name