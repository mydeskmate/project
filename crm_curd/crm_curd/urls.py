"""crm_curd URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from app01 import views
from curd_admin.service import v1

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^test/', views.test),
    # url(r'^test/', include('app01.urls')),
    # url(r'^test/', ([
    #                     url(r'^test/', views.test),
    #                     url(r'^test/', views.test),
    #                     url(r'^test/', views.test),
    #                     url(r'^test/', views.test),
    #                 ],"appname",'namespace')),
    # include,如果参数是模块路径？导入模块,找打urlpatterns对象的列表
    url(r'^curd_admin/', v1.site.urls),
    # url(r'^ttttttt/', views.tttttt,name='tt'),
]
