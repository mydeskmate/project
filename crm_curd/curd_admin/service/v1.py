from django.shortcuts import HttpResponse, render


class BaseCurdAdmin(object):
    """
    modle管理类
    """
    list_display = "__all__"

    # list_display = ['id','name','title']

    def __init__(self, model_class, site):
        self.model_class = model_class
        self.site = site
        self.request = None

    @property
    def urls(self):
        from django.conf.urls import url, include
        info = self.model_class._meta.app_label, self.model_class._meta.model_name
        urlpatterns = [
            url(r'^$', self.changelist_view, name='%s_%s_changelist' % info),
            url(r'^add/$', self.add_view, name='%s_%s_add' % info),
            url(r'^(.+)/delete/$', self.delete_view, name='%s_%s_delete' % info),
            url(r'^(.+)/change/$', self.change_view, name='%s_%s_change' % info),
        ]
        return urlpatterns

    def changelist_view(self, request):
        """
        查看列表
        :param reuqest:
        :return:
        """
        self.request = request
        result_list = self.model_class.objects.all()
        context = {
            'result_list': result_list,
            'list_display': self.list_display,
            "curd_admin_obj": self
        }
        return render(request, 'curd_admin/change_list.html', context)

    def add_view(self, reuqest):
        """
        添加数据
        :param reuqest:
        :return:
        """
        info = self.model_class._meta.app_label, self.model_class._meta.model_name
        data = "%s_%s_add" % info
        return HttpResponse(data)

    def delete_view(self, reuqest, pk):
        """
        删除
        :param reuqest:
        :param pk:
        :return:
        """
        # self.model_class.objects.filter(id=pk).delete()
        info = self.model_class._meta.app_label, self.model_class._meta.model_name
        data = "%s_%s_del" % info
        return HttpResponse(data)

    def change_view(self, reuqest, pk):
        """
        修改
        :param reuqest:
        :param pk:
        :return:
        """
        info = self.model_class._meta.app_label, self.model_class._meta.model_name
        data = "%s_%s_change" % info
        return HttpResponse(data)


class CurdAdminSite(object):
    """
    site类:注册module,自动生产url
    """
    def __init__(self):
        self._registry = {}
        self.namespace = "curd_admin"
        self.app_name = "curd_admin"

    def register(self, model_class, xxxxx=BaseCurdAdmin):
        """
        注册moudle类
        :param model_class:
        :param xxxxx:
        :return:
        """
        self._registry[model_class] = xxxxx(model_class, self)
        """
        {
            UserInfo类:  BaseCurdAdmin(UserInfo类,CurdAdminSite对象) # CurdAdminUserInfo(UserInfo类,CurdAdminSite对象)
            Role类:  BaseCurdAdmin(Role类,CurdAdminSite对象)
            XX类:  BaseCurdAdmin(XX类,CurdAdminSite对象)
        }

        """

    def get_urls(self):
        """动态生产url"""
        from django.conf.urls import url, include
        ret = [
            url(r'^login/', self.login, name='login'),
            url(r'^logout/', self.logout, name='logout'),
        ]
        for model_cls, curd_admin_obj in self._registry.items():
            app_label = model_cls._meta.app_label
            model_name = model_cls._meta.model_name

            print(app_label, model_name)

            ret.append(url(r'^%s/%s/' % (app_label, model_name), include(curd_admin_obj.urls)))
            # url(r'^admin/', admin.site.urls),
            # url(r'^test/', views.test),
            # url(r'^test/', include('app01.urls')),
            # url(r'^test/', ([
            #                     url(r'^test/', views.test),
            #                     url(r'^test/', views.test),
            #                     url(r'^test/', views.test),
            #                     url(r'^test/', views.test),
            #                 ],"appname",'namespace')),
            # include,如果参数是模块路径？导入模块,找打urlpatterns对象的列表

        return ret

    @property
    def urls(self):
        return self.get_urls(), self.app_name, self.namespace

    def login(self, request):
        return HttpResponse('login')

    def logout(self, request):
        return HttpResponse('logout')


site = CurdAdminSite()