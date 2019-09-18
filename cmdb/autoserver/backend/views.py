import json
from django.shortcuts import render,HttpResponse
from repository import models

# Create your views here.
def curd(requests):
    return render(requests,'curd.html')

def curd_json(requests):
    # 自定义表格数据配置
    table_config = [
        {'q':'id','title':'ID'},
        {'q':'hostname','title':'主机名'},
        {'q': 'create_at', 'title': '创建时间'},
        {'q': 'asset__cabinet_num', 'title': '机柜号'},
        {'q': 'asset__business_unit__name', 'title': '业务线名称'},
    ]

    # 获取表字段，和数据库中字段保持一致,可以跨表
    values_list = []
    for row in table_config:
        values_list.append(row['q'])

    from datetime import datetime
    from datetime import date
    # json 扩展; 支持时间序列化
    class JsonCustomEncoder(json.JSONEncoder):

        def default(self, value):
            if isinstance(value, datetime):
                return value.strftime('%Y-%m-%d %H:%M:%S')
            elif isinstance(value, date):
                return value.strftime('%Y-%m-%d')
            else:
                return json.JSONEncoder.default(self, value)

    server_list = models.Server.objects.values(*values_list)
    ret = {
        'server_list':list(server_list),
        'table_config':table_config
    }
    data = json.dumps(ret,cls=JsonCustomEncoder)               # 自定义json 序列化类
    return HttpResponse(data)