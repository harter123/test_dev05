from django.db import models
from app_api.models.h_test_hub.h_test_hub_model import HTestHub
from app_api.models.h_test_hub.h_module_model import HTestCaseModule
from django.contrib.auth.models import User

class HTestCase(models.Model):
    """
    模块表
    """
    h_test_hub = models.ForeignKey(HTestHub, on_delete=models.CASCADE)
    h_test_module = models.ForeignKey(HTestCaseModule, on_delete=models.CASCADE)
    title = models.CharField("描述", max_length=300, null=False, default="")
    pre_step = models.TextField("前置条件", default="")
    step = models.TextField("描述", default="")
    post_step = models.TextField("后置条件", default="")
    expect = models.TextField("预期结果", default="")
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    status_id = models.IntegerField("状态", default=0, null=False)
    priority_id = models.IntegerField("优先级", default=0, null=False)
    type_id = models.IntegerField("类型", default=0, null=False)

    is_delete = models.BooleanField("删除", default=False)
    update_time = models.DateTimeField("更新时间", auto_now=True)
    create_time = models.DateTimeField("创建时间", auto_now_add=True)

    def __str__(self):
        return self.name
