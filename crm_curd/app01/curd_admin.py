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
            tag = "<input name='pk' type='checkbox' value='{0}' />".format(obj.pk)
            return mark_safe(tag)

    def comb(self,obj=None,is_header=False):
        if is_header:
            return "组合列"
        else:
            return "%s-%s" %(obj.username,obj.email,)

    list_display = [checkbox,'id','username','email',comb,func,]

    def initial(self,request):
        """
        :param request:
        :return:
            True, /yg/app01/userinfo/?page=1&id=666&name=fangshaowei
            False, /yg/app01/userinfo/
        """
        pk_list = request.POST.getlist('pk')
        models.UserInfo.objects.filter(pk__in=pk_list).update(username='默认名字')
        return True

    initial.text = "初始化"

    def multi_del(self,request):
        pass

    multi_del.text = "批量删除"

    action_list = [initial,multi_del]

    from curd_admin.utils.filter_code import FilterOption

    def email(self, option, request):
        from curd_admin.utils.filter_code import FilterList
        queryset = models.UserInfo.objects.filter(id__gt=2)
        return FilterList(option, queryset, request)

    filter_list = [
        FilterOption('username', False, text_func_name="text_username", val_func_name="value_username"),
        FilterOption(email, False, text_func_name="text_email", val_func_name="value_email"),
        FilterOption('ug', True),
        FilterOption('mmm', False),
    ]
    # 1.取数据，放在页面上？
    #  username -> UserInfo表取数据
    #  ug       -> UserGroup表
    #  mmm      -> Role表
    # 2.单选和多选自定义
    # reuqest.GET    {'fk': [6,],'username': ['大刘']}
    # reuqest.GET.urlencode()
    # 注意注意注意：
    # 保留当前URL条件 + 自身条件
    # - 单选： /arya/app01/userinfo/?mm=2&fk=2&username=大刘
    # - 多选： /arya/app01/userinfo/?mm=2&fk=2&username=大刘     fk=7
    # reverse + reuqest.GET.urlencode()
v1.site.register(models.UserInfo,CurdAdminUserInfo)
# v1.site.register(models.UserInfo)

class CurdAdminRole(v1.BaseCurdAdmin):
    list_display = ['id','name',]
v1.site.register(models.Role,CurdAdminRole)

v1.site.register(models.UserGroup)