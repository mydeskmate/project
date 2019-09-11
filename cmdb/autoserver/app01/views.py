from django.shortcuts import render,HttpResponse

def asset(request):
    if request.method == "POST":
        print(request.POST)
        # 写入到数据
        return HttpResponse('1002')
    else:
        return HttpResponse('姿势不对')