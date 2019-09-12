import json
from django.shortcuts import render,HttpResponse
from repository import models

# Create your views here.
def asset(request):
    if request.method == "POST":
        # print(request.POST)
        # print(request.body)
        # 新资产信息
        server_info = json.loads(request.body.decode('utf-8'))
        hostname = server_info['basic']['data']['hostname']
        # 老资产信息
        server_obj = models.Server.objects.filter(hostname=hostname).first()
        if not server_obj:
            return HttpResponse('当前主机在资产中未录入！')


        # #########################处理磁盘信息#########################
        if not server_info['disk']['status']:
            models.ErrorLog.objects.create(content=server_info['disk']['data'],asset_obj=server_obj.asset,title='[%s]硬盘采集信息错误'%hostname)
        new_disk_dict = server_info['disk']['data']
        old_disk_lit = models.Disk.objects.filter(server_obj=server_obj)

        new_slot_list = list(new_disk_dict.keys())
        old_slot_list = []
        for item in old_disk_lit:
            old_slot_list.append(item.slot)

        update_list = set(new_slot_list).intersection(old_slot_list)
        create_list = set(new_slot_list).difference(old_slot_list)
        del_list = set(old_slot_list).difference(new_slot_list)

        # 删除
        models.Disk.objects.filter(server_obj=server_obj,slot__in=del_list).delete()
        # 记录日志
        models.AssetRecord.objects.create(asset_obj=server_obj.asset,content="移除硬盘：%s"%(",".join(del_list)))






        for k,v in server_info.items():
            print(k,v)
        # 写入到数据
    return HttpResponse('...')
