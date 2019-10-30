from django.template import Library
from types import FunctionType
register = Library()


def table_body(result_list,list_display,curd_admin_obj):
    for row in result_list:
        if list_display == "__all__":
            yield [str(row),]
        else:
            # yield [getattr(row, name) for name in list_display]
            yield [ name(curd_admin_obj,row) if isinstance(name,FunctionType) else getattr(row, name)  for name in list_display]

def table_head(list_display,curd_admin_obj):
    if list_display == '__all__':
        yield "对象列表"
    else:
        for item in list_display:
            if isinstance(item, FunctionType):
                yield item(curd_admin_obj, is_header=True)
            else:
                # header_list.append(item)
                # item是什么类型？ "username"   "email"   "id"
                # 通过字符串获取对应的表字段对象
                yield curd_admin_obj.model_class._meta.get_field(item).verbose_name

@register.inclusion_tag("curd_admin/moudle_list.html")
def func(result_list, list_display,curd_admin_obj):
    v = table_body(result_list,list_display,curd_admin_obj)
    h = table_head(list_display, curd_admin_obj)
    # for item in list_display:
    #     # print(item,curd_admin_obj.model_class)  数据放到表头
    #     if isinstance(item,FunctionType):
    #         print(item.__name__.title())
    #     else:
    #         print(item)
    return {'xxxxx': v, 'header_list': h}