import json
import hashlib
import time
from django.shortcuts import render,HttpResponse
from repository import models
from django.conf import settings

#api key列表，过期删除
api_key_record = {
# "1b96b89695f52ec9de8292a5a7945e38|1501472467.4977243":1501472477.4977243
}

def decrypt(msg):
    from Crypto.Cipher import AES
    key = b'dfdsdfsasdfdsdfs'
    cipher = AES.new(key, AES.MODE_CBC, key)
    result = cipher.decrypt(msg) # result = b'\xe8\xa6\x81\xe5\x8a\xa0\xe5\xaf\x86\xe5\x8a\xa0\xe5\xaf\x86\xe5\x8a\xa0sdfsd\t\t\t\t\t\t\t\t\t'
    data = result[0:-result[-1]]
    return str(data,encoding='utf-8')

# Create your views here.
def asset(request):
    # for k,v in request.META.items():
    #     print(k,v)
    client_md5_time_key = request.META.get('HTTP_OPENKEY')
    client_md5_key,client_time = client_md5_time_key.split('|')
    client_time = float(client_time)
    server_time = time.time()

    # 第一关
    if server_time - client_time > 10:
        return HttpResponse('[第一关] 时间太长了，骗谁呢？')
    # 第二关
    temp = "%s|%s" %(settings.AUTH_KEY,client_time)
    m = hashlib.md5()
    m.update(bytes(temp,encoding='utf-8'))
    server_md5_key = m.hexdigest()
    if server_md5_key != client_md5_key:
        return HttpResponse('[第二关] key变了，你改内容了吧，哈哈')
    # 删除过期的key
    for k in list(api_key_record.keys()):
        v = api_key_record[k]
        if server_time > v:
            del api_key_record[k]


    # 第三关  key已经被用过
    if client_md5_time_key in api_key_record:
        return HttpResponse('[第三关] 有人已经用过这个key了，不能重复使用，嘻嘻')
    else:
        api_key_record[client_md5_time_key] = client_time + 10


    # 静态令牌
    # key = request.META.get('HTTP_OPENKEY')
    # if key != settings.AUTH_KEY:
    #     return HttpResponse('认证失败....')
    # 动态令牌
    # if server_md5_key != client_md5_key:
    #     return HttpResponse('认证失败...')

    if request.method == "GET":
        return HttpResponse('重要数据，没有权限不能查看')
    if request.method == "POST":
        # print(request.POST)
        # print(request.body)
        # return HttpResponse('Post收到了')

        server_info = decrypt(request.body)
        server_info = json.loads(server_info)
        # print(server_info)
        # return HttpResponse('Post收到了')
        # 新资产信息
        # server_info = json.loads(request.body.decode('utf-8'))
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
