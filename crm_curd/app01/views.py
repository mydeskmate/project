from django.shortcuts import render,HttpResponse
from django.urls import reverse
# Create your views here.

def tttttt(request):
    return HttpResponse('....')


def test(request):
    # 反向生成URL
    # include导入其他文件路径include('app01.urls',namespace='aaa')
    # app01.urls
    #           xxxx  name=xxx,
    # url = reverse('curd_admin:login')
    # print(url)

    # url = reverse('tt')
    # print(url)

    # /yg/app01/userinfo/add/
    # /yg/app02/xx/add/
    url = reverse('curd_admin:app02_xx_add')
    print(url)

    return HttpResponse('...')