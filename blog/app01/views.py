from django.shortcuts import render,HttpResponse,redirect
from django.forms import Form
from django.forms import fields
from django.forms import widgets
from app01 import models
from utils.pager import PageInfo
# Create your views here.

def index(request,*args,**kwargs):

    username = request.session.get('username')
    nickname = request.session.get('nickname')
    if not username:
        session_stat = 0
    else:
        session_stat =1

    #分类查找文章表
    type_choice_list = models.Article.type_choices
    condition = {}
    type_id = int(kwargs.get('type_id')) if kwargs.get('type_id') else None
    if type_id:
        condition['article_type_id'] = type_id
    article_list = models.Article.objects.filter(**condition)

    #分页
    all_count = article_list.count()
    page_info = PageInfo(request.GET.get('page'),all_count,5,'/index.html',11)
    article_list_page = article_list[page_info.start():page_info.end()]

    return render(request,'index.html',
    {
        'type_id':type_id,
        'type_choice_list':type_choice_list,
        'article_list_page':article_list_page,
        'page_info': page_info,
        'session_stat':session_stat,
        'nickname':nickname
    })


class LoginForm(Form):
    username = fields.CharField(
        max_length=18,
        min_length=6,
        error_messages={
            'required':'用户名不能为空',
            'min_length':'长度不能小于6位',
            'max_length':'长度不能多余18位'
        },
        widget=widgets.TextInput(attrs={'class':'form-control'})
    )
    password = fields.CharField(
        min_length=6,
        error_messages={
            'required':'密码不能为空',
            'min_length':'密码不能少于6位'
        },
        widget=widgets.TextInput(attrs={'class':'form-control'})
    )
    code = fields.CharField(widget=widgets.TextInput(attrs={'class':'form-control'}))



def login(request):
    if request.method == 'GET':
        obj = LoginForm()
        return render(request,'login.html',{'obj':obj})
    else:
        obj = LoginForm(request.POST)
        input_code = request.POST.get('code')
        session_code = request.session.get('code')

        if obj.is_valid():
            if input_code.upper() == session_code:
                obj.cleaned_data.pop('code')
                print(obj.cleaned_data)
                res = models.UserInfo.objects.filter(**obj.cleaned_data).first()
                if res:
                    request.session['username'] = res.username
                    request.session['nickname'] = res.nickname
                    return redirect('/')
                else:
                    return render(request,'login.html',{'obj':obj})
            else:
                return render(request,'login.html',{'obj':obj,'msg':'验证码不正确'})
        else:
            return render(request,'login.html',{'obj':obj})

def check_code(request):
    from io import BytesIO
    from utils.random_check_code import rd_check_code
    img, code = rd_check_code()
    print(code)
    stream = BytesIO()
    img.save(stream,'png')
    request.session['code'] = code
    return HttpResponse(stream.getvalue())

from app01.forms import RegisterForm

def register(request):
    if request.method == 'GET':
        obj = RegisterForm(request)
        return render(request,'register.html',{'obj':obj})
