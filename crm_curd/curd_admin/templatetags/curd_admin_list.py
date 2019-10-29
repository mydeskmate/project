from django.template import Library
from types import FunctionType
register = Library()


def table_body(result_list,list_display,curd_admin_obj):
    for row in result_list:
        # yield [getattr(row, name) for name in list_display]
        yield [ name(curd_admin_obj,row) if isinstance(name,FunctionType) else getattr(row, name)  for name in list_display]

def table_head(arg):
    pass

@register.inclusion_tag("curd_admin/moudle_list.html")
def func(result_list, list_display,curd_admin_obj):
    v = table_body(result_list,list_display,curd_admin_obj)

    for item in list_display:
        # print(item,curd_admin_obj.model_class)  数据放到表头
        if isinstance(item,FunctionType):
            print(item.__name__.title())
        else:
            print(item)
    return {'xxxxx':v}