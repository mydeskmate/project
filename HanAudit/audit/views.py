from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
import json
from audit import models
import random,string
import datetime
from audit import task_handler


# Create your views here.
@login_required
def index(request):
    return render(request,'index.html')

def acc_login(request):
    error = ''
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username,password=password)
        if user:
            login(request, user)    # 将user封装到request中 自动写入session
            return  redirect(request.GET.get('next') or  '/')
        else:
            error = "Wrong username or password!"
    return render(request,'login.html',{'error':error })

@login_required
def acc_logout(request):
    logout(request)

    return  redirect('/login/')

@login_required
def host_list(request):
    return render(request,'hostlist.html')



@login_required
def get_host_list(request):
    gid = request.GET.get('gid')
    if gid:
        if gid == '-1':#未分组
            host_list = request.user.account.host_user_binds.all()
        else:
            group_obj = request.user.account.host_groups.get(id=gid)
            host_list = group_obj.host_user_binds.all()

        data = json.dumps(list(host_list.values('id','host__hostname','host__ip_addr','host__port',
                                'host_user__username')))
        return HttpResponse(data)

@login_required
def get_token(request):
    """生成token并返回"""
    bind_host_id = request.POST.get('bind_host_id')
    time_obj =  datetime.datetime.now() - datetime.timedelta(seconds=300) #5mins ago
    exist_token_objs = models.Token.objects.filter(account_id=request.user.account.id,
                                                   host_user_bind_id=bind_host_id,
                                                   date__gt=time_obj )

    if exist_token_objs: # has token already
        token_data ={'token':exist_token_objs[0].val}
    else:
        token_val = ''.join(random.sample(string.ascii_lowercase+string.digits,8))

        token_obj = models.Token.objects.create(
            host_user_bind_id = bind_host_id,
            account = request.user.account,
            val = token_val
        )
        token_data = {'token':token_val}

    return HttpResponse(json.dumps(token_data))


@login_required
def multi_cmd(request):
    return render(request,'multi_cmd.html')


@login_required
def multitask(request):
    task_obj = task_handler.Task(request)
    if task_obj.is_valid():
        result = task_obj.run()
        return HttpResponse(json.dumps({'task_id':result}))
    return HttpResponse(json.dumps(task_obj.errors))


@login_required
def multitask_result(request):
    task_id = request.GET.get('task_id')
    # [ {
    #     'task_log_id':23.
    #     'hostname':
    #     'ipaddr'
    #     'username'
    #     'status'
    # } ]


    task_obj = models.Task.objects.get(id=task_id)

    results = list(task_obj.tasklog_set.values('id','status',
                                'host_user_bind__host__hostname',
                                'host_user_bind__host__ip_addr',
                                'result'
                                ))

    return HttpResponse(json.dumps(results))
