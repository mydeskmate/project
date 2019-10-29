from curd_admin.service import v1
from app01 import models
from django.utils.safestring import mark_safe


class CurdAdminUserInfo(v1.BaseCurdAdmin):
    def func(self,obj):
        # return "编辑"
        # return obj.username
        # primary_key
        # 反向生成 namespace
        from django.urls import reverse
        # print(obj,type(obj))
        # 当前app名称
        # 当前model名称
        # namespace名称
        # name = namespace:app名称_model名称_change
        # reverse()
        # print(self.model_class._meta.app_label,type(obj)._meta.app_label)
        # print(self.model_class._meta.model_name,type(obj)._meta.model_name)
        # from yingun.service import v1
        # print(self.site.namespace,v1.site.namespace)

        name = "{0}:{1}_{2}_change".format(self.site.namespace,self.model_class._meta.app_label,self.model_class._meta.model_name)
        url = reverse(name,args=(obj.pk,))
        return mark_safe("<a href='{0}'>编辑</a>".format(url))

    def checkbox(self,obj):
        tag = "<input type='checkbox' value='{0}' />".format(obj.pk)
        return mark_safe(tag)

    list_display = [checkbox,'id','username','email',func]

v1.site.register(models.UserInfo,CurdAdminUserInfo)


class CurdAdminRole(v1.BaseCurdAdmin):
    list_display = ['id','name',]

v1.site.register(models.Role,CurdAdminRole)