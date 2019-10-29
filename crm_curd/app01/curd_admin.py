from curd_admin.service import v1
from app01 import models

# class CurdAdminUserInfo(v1.BaseCurdAdmin):
#     pass
# v1.site.register(models.UserInfo,CurdAdminUserInfo)

v1.site.register(models.UserInfo)
v1.site.register(models.Role)