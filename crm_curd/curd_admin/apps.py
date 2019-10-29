from django.apps import AppConfig


class CurdAdminConfig(AppConfig):
    name = 'curd_admin'

    def ready(self):
        # 自动加载各应用下面的curd_admin模块,对moudle进行注册
        super(CurdAdminConfig, self).ready()

        from django.utils.module_loading import autodiscover_modules
        autodiscover_modules('curd_admin')

