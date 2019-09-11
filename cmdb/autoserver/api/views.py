import json
from django.shortcuts import render,HttpResponse


# Create your views here.
def asset(request):
    if request.method == "POST":
        # print(request.POST)
        # print(request.body)
        server_info = json.loads(request.body.decode('utf-8'))
        for k,v in server_info.items():
            print(k,v)
        # 写入到数据
    return HttpResponse('...')
