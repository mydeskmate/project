# from types import FunctionType
# def yuhao():
#     # print(obj.user)
#     return '小于浩'
#
# list_display = ('user', 'email', yuhao)
#
# for item in list_display:
#     # print(item,callable(item),isinstance(item,FunctionType))
#     if isinstance(item,FunctionType):
#         print(item())
#     else:
#         print(item)


def func(request, queryset):
    # print(request,queryset)
    return 111


func.short_description = "大于号"
actions = [func, ]

for item in actions:
    # Func, item(2,3)
    if hasattr(item,'short_description'):
        print(item.short_description,item(1,2))
    else:
        print(item.__name__.title(), item(1, 2))