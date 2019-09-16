import json
from django.shortcuts import render,HttpResponse
from repository import models
from django.conf import settings

# Create your views here.
def asset(request):
    for k,v in request.META.items():
        print(k,v)
    key = request.META.get('HTTP_OPENKEY')
    if key != settings.AUTH_KEY:
        return HttpResponse('认证失败....')

    if request.method == "GET":
        return HttpResponse('重要数据，没有权限不能查看')
    if request.method == "POST":
        # print(request.POST)
        # print(request.body)

        # 新资产信息
        server_info = json.loads(request.body.decode('utf-8'))
        hostname = server_info['basic']['data']['hostname']

        # for k,v in server_info.items():
        #     print(k,v)

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
        if del_list:
            models.Disk.objects.filter(server_obj=server_obj,slot__in=del_list).delete()
            # 记录日志
            models.AssetRecord.objects.create(asset_obj=server_obj.asset,content="移除硬盘：%s"%(",".join(del_list)))

        # 增加
        record_list = []
        for slot in create_list:
            disk_dict = new_disk_dict[slot]
            disk_dict['server_obj']  = server_obj
            models.Disk.objects.create(**disk_dict)
            temp = "新增硬盘：位置:{slot},容量:{capacity},型号:{model},类型:{pd_type}".format(**disk_dict)
            record_list.append(temp)
        if record_list:
            content = ";".join(record_list)
            models.AssetRecord.objects.create(asset_obj=server_obj.asset,content=content)

        # 更新
        record_list = []
        row_map = {'capacity':'容量','pd_type':'类型','model':'型号'}
        for slot in update_list:
            new_disk_row = new_disk_dict[slot]
            old_disk_row = models.Disk.objects.filter(slot=slot,server_obj=server_obj).first()
            for k,v in new_disk_row.items():
                value = getattr(old_disk_row,k)
                if v != value:
                    record_list.append("槽位%s,%s由%s变更为%s" %(slot,row_map[k],value,v))
                    setattr(old_disk_row,k,v)
            old_disk_row.save()
        if record_list:
            content = ";".join(record_list)
            models.AssetRecord.objects.create(asset_obj=server_obj.asset,content=content)







        for k,v in server_info.items():
            print(k,v)
        # 写入到数据
    return HttpResponse('...')
