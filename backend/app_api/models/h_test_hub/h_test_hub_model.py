from django.db import models
from django.contrib.auth.models import User


class HTestHub(models.Model):
    """
    测试库表
    """
    name = models.CharField("名称", max_length=100, null=False, default="")
    describe = models.TextField("描述", default="")
    flag = models.CharField("标识", max_length=20, null=False, default="")
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    h_test_plan_num = models.IntegerField("测试计划个数", default=0, null=False)
    is_delete = models.BooleanField("删除", default=False)
    update_time = models.DateTimeField("更新时间", auto_now=True)
    create_time = models.DateTimeField("创建时间", auto_now_add=True)

    def __str__(self):
        return self.name
