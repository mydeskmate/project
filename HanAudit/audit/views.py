from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
import json


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
