from django.db import models
from django.contrib.auth.models import User

from app_api.models.h_test_hub.h_test_hub_model import HTestHub


class HTestHubVisitedRecently(models.Model):
    """
    最近访问测试库表
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    h_test_hub = models.ForeignKey(HTestHub, on_delete=models.CASCADE)

    is_delete = models.BooleanField("删除", default=False)
    update_time = models.DateTimeField("更新时间", auto_now=True)
    create_time = models.DateTimeField("创建时间", auto_now_add=True)

    def __str__(self):
        return self.user.username
