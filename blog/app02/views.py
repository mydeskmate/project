from django.shortcuts import render,HttpResponse
from app02 import models

def login(request):
    if request.method == "GET":
        return render(request,'login_auth.html')
    else:
        # 指定该用户对应的权限和操作进行模型， 没有从数据库获取
        user_permission_dict = {
            '/index.html': ["GET","POST","DEL","Edit"],
            '/order.html':  ["GET","POST","DEL","Edit"],
            '/comments-(\d+).html':  ["GET","POST","DEL","Edit"],
        }

        request.session['user_permission_dict'] = user_permission_dict

        return HttpResponse('登录成功')

def index(request):
    # http://127.0.0.1:8000/auth_index.html?md=GET
    return HttpResponse('登陆，并且有权限才能看见我')