from django.shortcuts import render,HttpResponse,redirect
from django.forms import Form
from django.forms import fields
from django.forms import widgets
from django.db.models import Count
from django.db.models import F,Q
from django.db import transaction
from django.db.utils import IntegrityError
from app01 import models
from utils.pager import PageInfo
from pathlib import Path
import json
import os
import uuid


# Create your views here.

def index(request,*args,**kwargs):
    """
    首页
    :param request:
    :param args:
    :param kwargs:
    :return:
    """
    username = request.session.get('username')
    nickname = request.session.get('nickname')
    avatar = ""
    if not username:
        session_stat = 0
    else:
        session_stat =1
        user = models.UserInfo.objects.filter(username=username).first()
        avatar = "/" + str(user.avatar)

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
        'nickname':nickname,
        'user':user,
        'avatar':avatar
    })


class LoginForm(Form):
    username = fields.CharField(
        max_length=18,
        min_length=5,
        error_messages={
            'required':'用户名不能为空',
            'min_length':'长度不能小于5位',
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
        widget=widgets.TextInput(attrs={'class':'form-control','type':'password'})
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
                # print(obj.cleaned_data)
                res = models.UserInfo.objects.filter(**obj.cleaned_data).first()
                if res:
                    request.session['user_id'] = res.nid
                    request.session['username'] = res.username
                    request.session['nickname'] = res.nickname
                    # 有可能未创建博客
                    if hasattr(res,'blog'):
                        request.session['blog_id'] = res.blog.nid
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
    # print(code)
    stream = BytesIO()
    img.save(stream,'png')
    request.session['code'] = code
    return HttpResponse(stream.getvalue())

from app01.forms import RegisterForm
from django.core.exceptions import NON_FIELD_ERRORS

def register(request):
    if request.method == 'GET':
        # obj = RegisterForm(request)
        obj = RegisterForm(request)
        return render(request,'register.html',{'obj':obj})
    else:
        obj = RegisterForm(request,request.POST,request.FILES)
        if obj.is_valid():
            obj.cleaned_data.pop('code')
            obj.cleaned_data.pop('password2')
            user = models.UserInfo.objects.create(**obj.cleaned_data)
            # print(user.avatar)

            return redirect('/login/')
        else:
            print(obj.errors)
        return render(request,'register.html',{'obj':obj})


def home(request,site):
    blog = models.Blog.objects.filter(site=site).first()
    if not blog:
        return redirect('/')

    # 分类
    category_list = models.Article.objects.filter(blog=blog).values('category_id','category__title').annotate(ct=Count('nid'))
    # 标签
    tag_list = models.Article2Tag.objects.filter(article__blog=blog).values('tag_id','tag__title').annotate(ct=Count('id'))

    # 时间
    date_list = models.Article.objects.filter(blog=blog).extra(select={'ctime':"strftime('%%Y-%%m',create_time)"}).values('ctime').annotate(ct=Count('nid'))

    article_list = models.Article.objects.all()

    return render(
        request,
        'home.html',
        {
            'blog':blog,
            'category_list':category_list,
            'tag_list':tag_list,
            'date_list':date_list,
            'article_list':article_list,
        }
    )


def filter(request,site,key,val):
    """
    根据条件筛选文章
    :param request:
    :param site:
    :param key:
    :param val:
    :return:
    """
    blog = models.Blog.objects.filter(site=site).first()
    if not blog:
        return redirect('/')

    # 分类
    category_list = models.Article.objects.filter(blog=blog).values('category_id', 'category__title').annotate(
        ct=Count('nid'))

    # 标签
    tag_list = models.Article2Tag.objects.filter(article__blog=blog).values('tag_id', 'tag__title').annotate(
        ct=Count('id'))

    # 时间
    date_list = models.Article.objects.filter(blog=blog).extra(
        select={'ctime': "strftime('%%Y-%%m',create_time)"}).values('ctime').annotate(ct=Count('nid'))

    # print(val)
    # 筛选
    if key == 'category':
        if  not eval(val):
            # print(val)
            article_list = models.Article.objects.filter(blog=blog, category_id=None)
        else:
            article_list = models.Article.objects.filter(blog=blog, category_id=val)
    elif key == 'tag':
        article_list = models.Article.objects.filter(blog=blog,article2tag__tag=val)
    else:
        article_list = models.Article.objects.filter(blog=blog).extra(where=["strftime('%%Y-%%m',create_time)=%s"]
                                                                      ,params=[val,])
    return render(
        request,
        'filter.html',
        {
            'blog': blog,
            'category_list': category_list,
            'tag_list': tag_list,
            'date_list': date_list,
            'article_list': article_list,
        }
    )


def article(request,site,nid):
    blog = models.Blog.objects.filter(site=site).first()
    if not blog:
        return redirect('/')

    # 分类
    category_list = models.Article.objects.filter(blog=blog).values('category_id', 'category__title').annotate(
        ct=Count('nid'))

    # 标签
    tag_list = models.Article2Tag.objects.filter(article__blog=blog).values('tag_id', 'tag__title').annotate(
        ct=Count('id'))

    # 时间
    date_list = models.Article.objects.filter(blog=blog).extra(
        select={'ctime': "strftime('%%Y-%%m',create_time)"}).values('ctime').annotate(ct=Count('nid'))

    obj = models.Article.objects.filter(blog=blog,nid=nid).first()

    # ####################### 评论 #############################
    msg_list = [
        {'id': 1, 'content': '写的太好了', 'parent_id': None},
        {'id': 2, 'content': '你说得对', 'parent_id': None},
        {'id': 3, 'content': '顶楼上', 'parent_id': None},
        {'id': 4, 'content': '你眼瞎吗', 'parent_id': 1},
        {'id': 5, 'content': '我看是', 'parent_id': 4},
        {'id': 6, 'content': '鸡毛', 'parent_id': 2},
        {'id': 7, 'content': '你是没呀', 'parent_id': 5},
        {'id': 8, 'content': '惺惺惜惺惺想寻', 'parent_id': 3},
    ]
    msg_list_dict = {}
    for item in msg_list:
        item['child'] = []
        msg_list_dict[item['id']] = item

    # #### msg_list_dict用于查找,msg_list
    result = []
    for item in msg_list:
        pid = item['parent_id']
        if pid:
            msg_list_dict[pid]['child'].append(item)
        else:
            result.append(item)

    # ########################### 打印  后端处理多级评论###################
    from utils.comment import comment_tree
    comment_str = comment_tree(result)

    # print(comment_str)
    return render(
        request,
        'article.html',
        {
            'blog': blog,
            'category_list': category_list,
            'tag_list': tag_list,
            'date_list': date_list,
            'obj':obj,
            "comment_str":comment_str
        }
    )

def comments(request,nid):
    """
    前端处理多级评论，将层级结构传递给前端
    :param request:
    :param nid:
    :return:
    """
    response = {'status':True,'data':None,'msg':None}
    try:
        # msg_list = [
        #     {'id':1,'content':'写的太好了','parent_id':None},
        #     {'id':2,'content':'你说得对','parent_id':None},
        #     {'id':3,'content':'顶楼上','parent_id':None},
        #     {'id':4,'content':'你眼瞎吗','parent_id':1},
        #     {'id':5,'content':'我看是','parent_id':4},
        #     {'id':6,'content':'鸡毛','parent_id':2},
        #     {'id':7,'content':'你是没呀','parent_id':5},
        #     {'id':8,'content':'惺惺惜惺惺想寻','parent_id':3},
        # ]

        # 修改列名 以符合上面的格式
        msg_list_queryset = models.Comment.objects.filter(article_id=nid).extra(select={'parent_id':'reply_id','id':'nid'}).values('id','content','parent_id')
        msg_list = list(msg_list_queryset)
        # print(msg_list)


        msg_list_dict = {}
        for item in msg_list:
            item['child'] = []
            msg_list_dict[item['id']] = item
        result = []
        for item in msg_list:
            pid = item['parent_id']
            if pid:
                msg_list_dict[pid]['child'].append(item)
            else:
                result.append(item)
        response['data'] = result
    except Exception as e:
        response['status'] = False
        response['msg'] = str(e)
    return HttpResponse(json.dumps(response))


def up(request):
    response = {'status':1006,'msg':None}
    try:
        user_id = request.session.get('user_id')
        article_id = request.POST.get('nid')
        val = int(request.POST.get('val'))
        obj = models.UpDown.objects.filter(user_id=user_id,article_id=article_id).first()
        if obj:
            pass
        else:
            # print(val)
            # print(user_id,article_id)

            with transaction.atomic():
                if val:
                    models.UpDown.objects.create(user_id=user_id, article_id=article_id, up=True)
                    models.Article.objects.filter(nid=article_id).update(up_count=F('up_count') + 1)
                else:
                    models.UpDown.objects.create(user_id=user_id, article_id=article_id, up=False)
                    models.Article.objects.filter(nid=article_id).update(down_count=F('down_count') + 1)
                    response['status'] = 1007
    except Exception as e:
        response['status'] = False
        response['msg'] = str(e)

    return HttpResponse(json.dumps(response))


def shaixuan(request,**kwargs):
    """
    组合筛选
    :param request:
    :return:
    """
    # print(kwargs)

    path = request.path_info
    condition = {}
    for k,v in kwargs.items():
        kwargs[k] = int(v)    #类型转换， 否则前端比较时，不相等
        if v != '0':
            condition[k] = v
    # print(condition)
    blog_id = request.session.get('blog_id')
    # 大分类
    type_list = models.Article.type_choices

    # 个人分类
    category_list = models.Category.objects.filter(blog_id=blog_id)

    # 个人标签
    tag_list = models.Tag.objects.filter(blog_id=blog_id)

    # 进行筛选
    condition['blog_id'] = blog_id
    article_list = models.Article.objects.filter(**condition)

    # 分页
    all_count = article_list.count()
    page_info = PageInfo(request.GET.get('page'), all_count, 5,path, 11)
    article_list_page = article_list[page_info.start():page_info.end()]

    return render(
        request,
        'back/shaixuan.html',
        {
            'type_list':type_list,
            'category_list':category_list,
            'tag_list':tag_list,
            # 'article_list':article_list,
            'article_list_page': article_list_page,
            'page_info':page_info,
            'kwargs':kwargs
        }
    )

def del_article(request,nid):
    blog_id = request.session.get('blog_id')
    obj = models.Article.objects.filter(nid=nid,blog_id=blog_id)
    print(obj)
    models.Article.objects.filter(nid=nid,blog_id=blog_id).delete()
    return redirect("../shaixuan-0-0-0.html")



def article_detail(request,nid):
    """
    使用编辑取代
    :param request:
    :param nid:
    :return:
    """
    obj = models.Article.objects.filter(nid=nid).first()
    return render(request,'back/article_detail.html',{'obj':obj})





## kindeditor使用
from app01.forms import ArticleForm
def article_tijiao(request):
    """
    提交文章
    :param request:
    :return:
    """
    blog_id = request.session.get('blog_id')
    if request.method == 'GET':
        obj = ArticleForm(request)
        # print(obj)
        # return  HttpResponse("4444444444444")
        return render(request, 'back/article_tijiao.html', {'obj':obj})
    else:
        obj = ArticleForm(request,request.POST)
        if obj.is_valid():
            # content = obj.cleaned_data['content']
            # print(content)
            article_title = obj.cleaned_data['title']
            article_summary = obj.cleaned_data['summary']
            type_id = obj.cleaned_data['type']
            category_id = obj.cleaned_data['category']
            tags_id = obj.cleaned_data['tags']
            article_detail = obj.cleaned_data['content']

            with transaction.atomic():
                article = models.Article.objects.create(blog_id=blog_id,title=article_title,summary=article_summary,
                                                        article_type_id=type_id,category_id=category_id)
                models.ArticleDetail.objects.create(article_id=article.nid,content=article_detail)
                for tag in tags_id:
                    models.Article2Tag.objects.create(article_id=article.nid,tag_id=tag)
            return redirect("/back/shaixuan-0-0-0.html")


def edit_article(request,nid):
    """
    编辑文章
    :param request:
    :param nid:
    :return:
    """
    blog_id = request.session.get('blog_id')
    if request.method == "GET":
        # article = models.Article.objects.filter(nid=nid, blog_id=blog_id).extra(select={'type':'article_type_id','category':'category_id'}).values('title','summary','type',
        #                                              'category','articledetail__content')

        article = models.Article.objects.filter(nid=nid, blog_id=blog_id).first()
        art_dict = {'title':article.title,'summary':article.summary,'type':article.article_type_id,
                    'category':article.category_id,'content':article.articledetail.content}

        article_tags = article.tags.values_list('nid')
        # print(article_tags)
        # print(list(zip(*article_tags)))
        # print(list(zip(*article_tags))[0])
        article_tuple = list(zip(*article_tags))[0] if list(zip(*article_tags)) else []
        article_list = list(article_tuple)
        # print(article_list)
        art_dict['tags'] = article_list
        # print(art_dict)
        obj = ArticleForm(request,initial=art_dict)
        return render(request,'back/edit_article.html',{
            'obj':obj,
            'nid':nid
        })
    else:
        obj = ArticleForm(request, request.POST)
        if obj.is_valid():
            # print(obj.cleaned_data)
            article_title = obj.cleaned_data['title']
            article_summary = obj.cleaned_data['summary']
            type_id = obj.cleaned_data['type']
            category_id = obj.cleaned_data['category']
            tags_id = obj.cleaned_data['tags']
            article_detail = obj.cleaned_data['content']
            # print(article_detail)
            with transaction.atomic():
                article = models.Article.objects.filter(blog_id=blog_id,nid=nid).update(title=article_title,
                                            summary=article_summary,article_type_id=type_id, category_id=category_id)
                models.ArticleDetail.objects.filter(article_id=nid).update(content=article_detail)

                try:
                    for tag in tags_id:
                        if not models.Article2Tag.objects.filter(article_id=nid, tag_id=tag).filter():
                            models.Article2Tag.objects.create(article_id=nid, tag_id=tag)
                    models.Article2Tag.objects.exclude(article_id=nid, tag_id__in=tags_id).delete()
                except IntegrityError as e:
                    print(str(e))

            return redirect("/back/shaixuan-0-0-0.html")





def upload_img(request):
    """
    indeditor中上传图片
    :param request:
    :return:
    """
    import os
    import json
    upload_type = request.GET.get('dir')     #获取上传文件类型
    file_obj = request.FILES.get('imgFile')
    file_path = os.path.join('static/images',file_obj.name)
    with open(file_path,'wb') as f:
        for chunk in file_obj.chunks():
            f.write(chunk)

    dic = {
        'error':0,
        'url':'/' + file_path,
        'message':'错误了'
    }
    return HttpResponse(json.dumps(dic))



def category(request):
    path = request.path_info
    blog_id = request.session.get('blog_id')
    if request.method == 'GET':

        # category_list = models.Article.objects.filter(blog_id=blog_id).values('category_id', 'category__title').annotate(
        #     ct=Count('nid'))

        category_list = models.Category.objects.filter(blog_id=blog_id).values('nid','title').annotate(ct = Count('article__nid'))

        # 分页
        all_count = category_list.count()
        page_info = PageInfo(request.GET.get('page'), all_count, 5, path, 11)
        category_list_page = category_list[page_info.start():page_info.end()]

        return render(request,'back/category.html',
                      {
                          'category_list_page':category_list_page,
                          'page_info': page_info,
                      })


def category_add(request):
    blog_id = request.session.get('blog_id')
    if request.method == 'POST':
        title = request.POST.get('title')
        if title:
            models.Category.objects.create(title=title,blog_id=blog_id)
        return redirect('/back/category.html')


def del_categroy(request,nid):
    blog_id = request.session.get('blog_id')
    if request.method == "GET":
        models.Category.objects.filter(blog_id=blog_id,nid=nid).delete()
    return redirect('/back/category.html')

def edit_category(request,nid):
    """
    处理通过ajax提交的数据
    :param request:
    :param nid:
    :return:
    """
    blog_id = request.session.get('blog_id')
    category_obj = models.Category.objects.filter(nid=nid).first()
    if request.method == 'GET':
        return render(request,'back/edit_category.html',{'obj':category_obj})
    else:
        ret = {'status': 1, 'message': None}
        try:
            title = request.POST.get('title')
            # print(title)
            models.Category.objects.filter(blog_id=blog_id,nid=nid).update(title=title)
        except Exception as e:
            ret['status'] = False
            ret['message'] = str(e)
        return HttpResponse(json.dumps(ret))


def tag(request):
    path = request.path_info
    blog_id = request.session.get('blog_id')
    if request.method == 'GET':
        # tag_list = models.Article.objects.filter(blog_id=blog_id).values('tags__nid','tags__title').annotate(
        #     ct = Count('nid')
        # )

        tag_list = models.Tag.objects.filter(blog_id=blog_id).values('nid','title').annotate(ct = Count('article2tag__article_id'))
        # print(tag_list.query)

        # 分页
        all_count = tag_list.count()
        page_info = PageInfo(request.GET.get('page'), all_count, 5, path, 11)
        tag_list_page = tag_list[page_info.start():page_info.end()]

        return render(request, 'back/tag.html',
                      {
                          'tag_list_page': tag_list_page,
                          'page_info': page_info,
                      })


def tag_add(request):
    msg = ""
    blog_id = request.session.get('blog_id')
    if request.method == 'POST':
        title = request.POST.get('title')
        if  title:
            models.Tag.objects.create(title=title,blog_id=blog_id)
        return redirect('/back/tag.html')


def del_tag(request,nid):
    blog_id = request.session.get('blog_id')
    if request.method == "GET":
        models.Tag.objects.filter(blog_id=blog_id,nid=nid).delete()
    return redirect('/back/tag.html')


def edit_tag(request,nid):
    """
    处理通过ajax提交的数据
    :param request:
    :param nid:
    :return:
    """
    blog_id = request.session.get('blog_id')
    tag_obj = models.Tag.objects.filter(nid=nid).first()
    if request.method == 'GET':
        return render(request,'back/edit_tag.html',{'obj':tag_obj})
    else:
        ret = {'status': 1, 'message': None}
        try:
            title = request.POST.get('title')
            # print(title)
            models.Tag.objects.filter(blog_id=blog_id,nid=nid).update(title=title)
        except Exception as e:
            ret['status'] = False
            ret['message'] = str(e)
        return HttpResponse(json.dumps(ret))

from app01.forms import UserinfoForm
def userinfo(request):
    nid = request.session.get('user_id')
    blog_id = request.session.get('blog_id')
    blog = models.Blog.objects.filter(nid=blog_id,user_id=nid).first()

    user_obj = models.UserInfo.objects.filter(nid=nid).first()
    if request.method == 'GET':
        user_dict = {
            'nickname':user_obj.nickname,
            'email':user_obj.email,
            'avatar':user_obj.avatar,
        }
        # 因为数据库存放的是相对路径，无法访问，转换为绝对路径
        avatar = "/" + str(user_obj.avatar)
        # print(avatar)
        if blog:
            user_dict['site'] = blog.site
            user_dict['theme'] = blog.theme
        obj = UserinfoForm(request,initial=user_dict)
        return render(request,'back/userinfo.html',{'obj':obj,'user_obj':user_obj,'avatar':avatar})
    else:
        obj = UserinfoForm(request,request.POST,request.FILES)
        if obj.is_valid():
            # 生成随机图片地址
            file_obj = request.FILES.get('avatar')
            file_name = file_obj.name
            ext = file_name.split('.')[-1]
            file_name_pre = file_name.split('.')[0]
            file_name = '{}{}.{}'.format(file_name_pre + "_", uuid.uuid4().hex[:7], ext)
            # 存入图片
            # file_path = os.path.join('static/images', file_name)
            file_path = "static/images/" + file_name

            with open(file_path, 'wb') as f:
                for chunk in file_obj.chunks():
                    f.write(chunk)

            # 删除原来的图片
            file_path_old = str(user_obj.avatar)
            if os.path.isfile(file_path_old):
                os.remove(file_path_old)

            nickname = obj.cleaned_data['nickname']
            email = obj.cleaned_data['email']
            site = obj.cleaned_data['site']
            theme = obj.cleaned_data['theme']
            with transaction.atomic():
                models.UserInfo.objects.filter(nid=nid).update(nickname=nickname,email=email,avatar=file_path)
                models.Blog.objects.filter(nid=blog_id,user_id=nid).update(site=site,theme=theme)

            return redirect('/back/userinfo.html')
        else:
            return HttpResponse('eeeeee')


def back(request):
    return redirect('/back/shaixuan-0-0-0.html')