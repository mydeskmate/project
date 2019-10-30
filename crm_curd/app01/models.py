from django.db import models

class Role(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name

class UserInfo(models.Model):

    username = models.CharField(max_length=32,verbose_name="用户名")
    email = models.CharField(max_length=32,verbose_name="邮箱")

