from django import template

register = template.Library()


@register.simple_tag
def my_avatar(arg1,arg2):
    """
    返回绝路路径的avatar
    :param value:
    :param arg:
    :return:
    """
    return arg1 + str(arg2)