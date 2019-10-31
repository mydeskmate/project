import copy
from django.shortcuts import HttpResponse,render,redirect
from django.urls import reverse

class BaseCurdAdmin(object):
    """
    modle管理类
    """
    list_display = "__all__"

    # list_display = ['id','name','title']

    add_or_edit_model_form = None

    def __init__(self, model_class, site):
        self.model_class = model_class
        self.site = site
        self.request = None

        self.app_label = model_class._meta.app_label
        self.model_name = model_class._meta.model_name

    def get_add_or_edit_model_form(self):
        """获取model Form"""
        if self.add_or_edit_model_form:
            return self.add_or_edit_model_form
        else:
            # 对象由累创建,累由type创建？
            from django.forms import ModelForm
            # class MyModelForm(ModelForm):  方法一：
            #     class Meta:
            #         model = self.model_class
            #         fields = "__all__"
            _m = type('Meta',(object,),{'model': self.model_class,'fields':"__all__"})   #方法二
            MyModelForm = type('MyModelForm',(ModelForm,),{"Meta": _m})
            return MyModelForm

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
        # 生成页面上：添加按钮
        from django.http.request import QueryDict
        param_dict = QueryDict(mutable=True)
        if request.GET:
            param_dict['_changelistfilter'] = request.GET.urlencode()

        base_add_url = reverse("{2}:{0}_{1}_add".format(self.app_label, self.model_name, self.site.namespace))
        add_url = "{0}?{1}".format(base_add_url, param_dict.urlencode())

        self.request = request
        # 分页 开始
        condition = {}

        from utils.my_page import PageInfo
        all_count = self.model_class.objects.filter(**condition).count()
        base_page_url = reverse("{2}:{0}_{1}_changelist".format(self.app_label, self.model_name, self.site.namespace))
        page_param_dict = copy.deepcopy(request.GET)
        page_param_dict._mutable = True

        page_obj = PageInfo(request.GET.get('page'), all_count, base_page_url, page_param_dict)
        result_list = self.model_class.objects.filter(**condition)[page_obj.start:page_obj.end]

        # 分页结束


        context = {
            'result_list': result_list,
            'list_display': self.list_display,
            "curd_admin_obj": self,
            'add_url': add_url,
            'page_str': page_obj.pager()
        }
        return render(request, 'curd_admin/change_list.html', context)

    def add_view(self,request):
        """
        添加数据
        :param reuqest:
        :return:
        """
        if request.method == 'GET':
            model_form_obj = self.get_add_or_edit_model_form()()
            context = {
                'form': model_form_obj
            }
            return render(request, 'curd_admin/add.html', context)
        else:
            model_form_obj = self.get_add_or_edit_model_form()(data=request.POST,files=request.FILES)
            if model_form_obj.is_valid():
                obj = model_form_obj.save()
                # 如果是popup，
                popid = request.GET.get('popup')
                if popid:
                    return render(request,'curd_admin/popup_response.html',{'data_dict':{ 'pk': obj.pk,'text': str(obj),'popid': popid} })
                else:
                    # 添加成功,进行跳转
                    # /yg/app01/userinfo/  +  request.GET.get('_changelistfilter')
                    base_list_url = reverse("{2}:{0}_{1}_changelist".format(self.app_label, self.model_name, self.site.namespace))
                    list_url = "{0}?{1}".format(base_list_url,request.GET.get('_changelistfilter') )
                    return redirect(list_url)

            context = {
                'form': model_form_obj
            }
            return render(request,'curd_admin/add.html',context)

    def delete_view(self,reuqest,pk):
        """
        删除
        :param reuqest:
        :param pk:
        :return:
        """
        # self.model_class.objects.filter(id=pk).delete()
        """
        根据pk获取数据，然后delete()
        # 获取url,跳转回列表页面
        """

        info = self.model_class._meta.app_label, self.model_class._meta.model_name
        data = "%s_%s_del" % info
        return HttpResponse(data)

    def change_view(self,request,pk):
        """
        修改
        :param reuqest:
        :param pk:
        :return:
        """
        # 1. 获取_changelistfilter中传递的参数
        # request.GET.get("_changelistfilter")
        # 2. 页面显示并提供默认值ModelForm
        obj = self.model_class.objects.filter(pk=pk).first()
        if not obj:
            return HttpResponse('ID不存在')
        if request.method == "GET":
            model_form_obj = self.get_add_or_edit_model_form()(instance=obj)
        else:
            model_form_obj = self.get_add_or_edit_model_form()(data=request.POST,files=request.FILES,instance=obj)
            if model_form_obj.is_valid():
                model_form_obj.save()
                base_list_url = reverse(
                    "{2}:{0}_{1}_changelist".format(self.app_label, self.model_name, self.site.namespace))
                list_url = "{0}?{1}".format(base_list_url, request.GET.get('_changelistfilter'))
                return redirect(list_url)
        # 3. 返回页面
        context = {
            'form': model_form_obj
        }

        return render(request,'curd_admin/edit.html',context)


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