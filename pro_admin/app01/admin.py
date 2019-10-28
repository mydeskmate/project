from django.http import HttpResponse
from django.contrib import admin
from app01 import models
from django.utils.safestring import mark_safe
# Register your models here.
from django.forms import ModelForm
from django.forms import fields
from django.forms import widgets
class MyForm(ModelForm):
    others = fields.CharField(widget=widgets.TextInput())
    user = fields.CharField(widget=widgets.TextInput(),error_messages={'required': '用户bunegn '})
    class Meta:
        model = models.UserInfo
        fields = "__all__"
        # ..
class UserInfoModelAdmin(admin.ModelAdmin):
    # def changelist_view(self, request, extra_context=None):
    #     return HttpResponse('新的列表视图')
    form = MyForm
    def haha(self):
        return mark_safe("<a href='http://www.baidu.com'>%s</a>" % (self.user))
    list_display = ('user','email',haha)
    list_filter = ('user',)
    list_editable = ('email',)
    search_fields = ('user',)
    preserve_filters = False

    def func(self,request,queryset):
        print(self,request,queryset)
        print(request.POST.getlist('_selected_action'))

    func.short_description = "函数"
    actions = [func,]
admin.site.register(models.UserInfo,UserInfoModelAdmin)
admin.site.register(models.UserGroup)
admin.site.register(models.Role)

"""
{
    models.UserInfo: admin.ModelAdmin(models.UserInfo,admin.site)
    models.UserGroup: admin.ModelAdmin(models.UserGroup,admin.site)
}
"""