from curd_admin.service import v1
from app01 import models
from django.utils.safestring import mark_safe
from django.urls import reverse

class CurdAdminUserInfo(v1.BaseCurdAdmin):
    def func(self,obj=None,is_header=False):
        if is_header:
            return '操作'
        else:
            # name = "{0}:{1}_{2}_change".format(self.site.namespace,self.model_class._meta.app_label,self.model_class._meta.model_name)
            # url = reverse(name,args=(obj.pk,))

            from django.http.request import QueryDict
            param_dict = QueryDict(mutable=True)
            if self.request.GET:
                param_dict['_changelistfilter'] =self.request.GET.urlencode()

            base_edit_url = reverse("{2}:{0}_{1}_change".format(self.app_label, self.model_name, self.site.namespace),args=(obj.pk,))
            edit_url = "{0}?{1}".format(base_edit_url,param_dict.urlencode())

            return mark_safe("<a href='{0}'>编辑</a>".format(edit_url))

    def checkbox(self, obj=None, is_header=False):
        if is_header:
            return "选项"
            # return mark_safe("<input type='checkbox'/>")
        else:
            tag = "<input type='checkbox' value='{0}' />".format(obj.pk)
            return mark_safe(tag)

    def comb(self,obj=None,is_header=False):
        if is_header:
            return "组合列"
        else:
            return "%s-%s" %(obj.username,obj.email,)

    list_display = [checkbox,'id','username','email',func,comb]

v1.site.register(models.UserInfo,CurdAdminUserInfo)
# v1.site.register(models.UserInfo)

class CurdAdminRole(v1.BaseCurdAdmin):
    list_display = ['id','name',]

v1.site.register(models.Role,CurdAdminRole)