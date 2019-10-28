from django.shortcuts import render,HttpResponse,redirect
from app01 import models
from django.template.response import TemplateResponse
from django.forms import Form,ModelForm
from django.forms import fields as ffields
from django.forms import widgets as fwidgets

"""
class TestForm(Form):
    user = fields.CharField()
    email = fields.EmailField()
    ug_id = fields.ChoiceField(
        widget=widgets.Select,
        choices=[]
    )

    def __init__(self,*args,**kwargs):
        super(TestForm,self).__init__(*args,**kwargs)

        self.fields['ug_id'].choices = models.UserGroup.objects.values_list('id','title')


def test(request):
    if request.method == "GET":
        form = TestForm()
        context = {
            'form': form
        }
        return render(request,'test.html',context)
    else:
        form = TestForm(request.POST)
        if form.is_valid():
            # {ug:1}
            models.UserInfo.objects.create(**form.cleaned_data)
            return redirect('http://www.oldboyedu.com')
        context = {
            'form': form
        }
        return render(request, 'test.html', context)
"""

class TestModelForm(ModelForm):
    # 覆盖model中user
    # user = ffields.EmailField(label='用户名')

    class Meta:
        model = models.UserInfo
        fields = "__all__"
        error_messages = {
            'user':{'required':'用户名不能为空'},
            'email':{'required':'邮箱不能为空','invalid':'邮箱格式错误'},
        }
        labels = {
            'user': '用户名',
            'email': "邮箱"
        }
        help_texts = {
            'user': "帮你一下"
        }
        # widgets = {
        #     'user': fwidgets.Textarea(attrs={'class':'c1'})
        # }
        # field_classes = {
        #     'user': ffields.EmailField
        # }

    # def clean_user(self):
    #     pass
    #
    # def clean_email(self):
    #     pass
def test(request):
    if request.method == "GET":
        form = TestModelForm()
        context = {
            'form': form
        }
        return render(request,'test.html',context)
    else:
        form = TestModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('http://www.oldboyedu.com')
        context = {
            'form': form
        }
        return render(request, 'test.html', context)


def edit(request,nid):
    obj = models.UserInfo.objects.filter(id=nid).first()
    if request.method == "GET":
        form = TestModelForm(instance=obj)
        context = {
            'form': form
        }
        return render(request, 'edit.html', context)
    else:
        form = TestModelForm(instance=obj,data=request.POST,files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect('http://www.oldboyedu.com')
        context = {
            'form': form
        }
        return render(request, 'test.html', context)
