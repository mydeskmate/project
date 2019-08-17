from django.shortcuts import render,redirect,HttpResponse
from web import models
from rbac import models as rbacmodels
from rbac.service import initial_permission
from utils.pager import PageInfo
import datetime
import json

# Create your views here.
def login(request):
    if request.method == "GET":
        return render(request,'login.html')
    else:
        u = request.POST.get('username')
        p = request.POST.get('password')
        obj = models.UserInfo.objects.filter(user__username=u,user__password=p).first()
        if obj:
            request.session['user_info'] = {'username':u,'nickname':obj.nickname,'nid':obj.id}
            initial_permission(request,obj.user_id)
            return redirect('/index.html')
        else:
            return render(request,'login.html')


def index(request):
    if not request.session.get('user_info'):
        return redirect('/login.html')

    return render(request,'index.html')


def trouble(request):
    """
    故障管理
    :param request:
    :return:
    """
    # request.permission_code_list
    if request.permission_code == "LOOK":
        trouble_list = models.Order.objects.filter(create_user_id=request.session['user_info']['nid'])

        # 分页
        all_count = trouble_list.count()
        page_info = PageInfo(request.GET.get('page'), all_count,5, '/trouble.html', 11)
        trouble_list_page = trouble_list[page_info.start():page_info.end()]
        return render(request,'trouble.html',
                      {
                          'trouble_list_page':trouble_list_page,
                          'page_info': page_info,
                      }
                      )

    elif request.permission_code == "DEL":
        nid = request.GET.get('nid')
        models.Order.objects.filter(create_user_id=request.session['user_info']['nid'],id=nid).delete()
        return redirect('/trouble.html')

    elif request.permission_code == "POST":
        if request.method == "GET":
            return render(request,'trouble_add.html')
        else:
            title = request.POST.get('title')
            content = request.POST.get('content')
            models.Order.objects.create(title=title,detail=content,create_user_id=request.session['user_info']['nid'])
            return redirect('/trouble.html')
    elif request.permission_code == "EDIT":
        if request.method == "GET":
            nid = request.GET.get('nid')
            obj = models.Order.objects.filter(create_user_id=request.session['user_info']['nid'],id=nid).first()
            return render(request,'trouble_edit.html',
                          {
                              'nid':nid,
                              'obj':obj,
                          }
                          )
        else:
            nid = request.GET.get('nid')
            title = request.POST.get('title')
            content = request.POST.get('content')
            models.Order.objects.filter(create_user_id=request.session['user_info']['nid'],id=nid).update(title=title,detail=content)
            return redirect('/trouble.html')
    elif request.permission_code == "DETAIL":
        if request.method == "GET":
            nid = request.GET.get('nid')
            obj = models.Order.objects.filter(create_user_id=request.session['user_info']['nid'], id=nid).first()
            return render(request, 'trouble_detail.html',
                          {
                              'nid': nid,
                              'obj': obj,
                          }
                          )


def trouble_kill(request):
    """
    报障单处理
    :param request:
    :return:
    """
    nid = request.session['user_info']['nid']
    if request.permission_code == "LOOK":
        # 查看列表:未解决,当前用户已经解决或正在解决
        from django.db.models import Q
        trouble_list = models.Order.objects.filter(Q(status=1)|Q(processor_id=nid)).order_by('status')

        # 分页
        all_count = trouble_list.count()
        page_info = PageInfo(request.GET.get('page'), all_count, 5, '/trouble-kill.html', 11)
        trouble_list_page = trouble_list[page_info.start():page_info.end()]
        return render(request, 'trouble_kill_look.html',
                      {
                          'trouble_list_page': trouble_list_page,
                          'page_info': page_info,
                      }
                      )



    elif request.permission_code == "EDIT":
        # http://127.0.0.1:8000/trouble-kill.html?md=edit&nid=1
        if request.method == 'GET':
            order_id = request.GET.get('nid')
            # 已经抢到了，未处理
            if models.Order.objects.filter(id=order_id,processor_id=nid,status=2):
                obj = models.Order.objects.filter(id=order_id).first()
                return render(request,'trouble_kill_edit.html',{'obj':obj})

            if models.Order.objects.filter(id=order_id,processor_id=nid,status=3):
                return HttpResponse("已处理，不能再处理了！！")

            # 开抢
            v = models.Order.objects.filter(id=order_id,status=1).update(processor_id=nid,status=2)
            if not v:
                return HttpResponse("小伙子，手速太慢了！！！")
            else:
                obj = models.Order.objects.filter(id=order_id).first()
                return render(request,'trouble_kill_edit.html',{'obj':obj})
        else:
            order_id = request.GET.get('nid')
            solution = request.POST.get('solution')
            models.Order.objects.filter(id=order_id,processor_id=nid).update(status=3,solution=solution,ptime=datetime.datetime.now())
            return redirect('/trouble-kill.html')
    elif request.permission_code == 'DEL':
        order_id = request.GET.get('nid')
        models.Order.objects.filter(id=order_id,processor_id=nid).delete()
        return redirect('/trouble-kill.html')
    elif request.permission_code == 'DETAIL':
        order_id = request.GET.get('nid')
        obj = models.Order.objects.filter(id=order_id).first()
        return render(request,'trouble_kill_detail.html',{'order_id':order_id,'obj':obj})

def report(request):
    """
    生成报表
    :param request:
    :return:
    """
    # print(request.permission_code)
    if request.permission_code  == "LOOK":
        if request.method == 'GET':
            return render(request,'report.html')
        else:
            from django.db.models import Count
            # 饼图
            result = models.Order.objects.filter(status=3).values_list('processor__nickname').annotate(ct=Count('id'))
            # print(result)
            # 分组：select * from xx group by processor_id,ptime(2017-11-11)
            # 折线图
            ymd_list = models.Order.objects.filter(status=3).extra(select={'ymd':"strftime('%%s',strftime('%%Y-%%m-%%d',ptime))"}).values('processor_id','processor__nickname','ymd').annotate(ct=Count('id'))
            ymd_dict = {}
            for row in ymd_list:
                key = row['processor_id']
                if key in ymd_dict:
                    ymd_dict[key]['data'].append([float(row['ymd'])*1000, row['ct']])
                else:
                    ymd_dict[key] = {'name':row['processor__nickname'],'data':[ [float(row['ymd'])*1000, row['ct']],  ]}
            response = {
                # 'pie': [['方少伟', 45.0],['吴永强',   40.0],['友情并',3],['尹树林',90]],
                'pie': list(result),
                'zhexian': list(ymd_dict.values())
            }
            # print(list(ymd_dict.values()))
            return HttpResponse(json.dumps(response))


def register(request):
    """
    注册用户
    :param request:
    :return:
    """
    if request.method == "GET":
        return render(request,'register.html')
    else:
        msg = ""
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            nickname = request.POST.get('nickname')
            email = request.POST.get('email')
            obj = rbacmodels.User.objects.filter(username=username).first()
            if obj:
                msg= "该用户已注册"
                return render(request,'register.html',{'msg':msg})
            else:
                from django.db import transaction
                with transaction.atomic():
                    row = rbacmodels.User.objects.create(username=username,password=password,email=email)
                    models.UserInfo.objects.create(nickname=nickname,user_id=row.id)
                return redirect('/login.html')
        except Exception as e:
            msg = str(e)
            return HttpResponse(msg)


def logout(request):
    if request.session.get('user_info'):
        request.session.clear()
        # request.session.delete(request.session.session_key)
    return redirect('/login.html')