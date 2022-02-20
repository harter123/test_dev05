from django.db import models
from app_api.models.h_test_hub.h_test_hub_model import HTestHub


class HTestCaseModule(models.Model):
    """
    模块表
    """
    h_test_hub = models.ForeignKey(HTestHub, on_delete=models.CASCADE)
    parent_id = models.IntegerField("父节点的id", null=False, default=0)
    name = models.CharField("名称", max_length=100, null=False, default="")
    is_delete = models.BooleanField("删除", default=False)
    update_time = models.DateTimeField("更新时间", auto_now=True)
    create_time = models.DateTimeField("创建时间", auto_now_add=True)

    def __str__(self):
        return self.name
