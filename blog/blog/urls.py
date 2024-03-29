"""blog URL Configuration

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
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from app01 import views
from app02 import views as views2

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'all/(?P<type_id>\d+)',views.index),
    url(r'^login',views.login),
    url(r'^auth_login',views2.login),
    url(r'^auth_index.html$',views2.index),
    url(r'^auth-menu.html$', views2.menu),

    url(r'^check_code',views.check_code),
    url(r'^register',views.register),
    url(r'^up.html$',views.up),

    url(r'^back/article_tijiao.html$', views.article_tijiao),
    url(r'^upload_img.html$', views.upload_img),
    url(r'^comments-(\d+).html$', views.comments),


    url(r'^back/shaixuan-(?P<article_type_id>\d+)-(?P<category_id>\d+)-(?P<tags__nid>\d+).html$', views.shaixuan),
    url(r'^back/del_article/(\d+).html$', views.del_article),
    url(r'^back/edit_article/(\d+).html$', views.edit_article),
    url(r'^back/category.html$', views.category),
    url(r'^back/category_add.html$', views.category_add),
    url(r'^back/del_categroy/(\d+).html$', views.del_categroy),
    url(r'^back/edit_category/(\d+).html$', views.edit_category),
    url(r'^back/tag.html$', views.tag),
    url(r'^back/tag_add.html$', views.tag_add),
    url(r'^back/del_tag/(\d+).html$', views.del_tag),
    url(r'^back/edit_tag/(\d+).html$', views.edit_tag),
    url(r'^back/userinfo.html$', views.userinfo),
    url(r'^back', views.back),


    # url(r'index.html', views.index),
    url(r'^(?P<site>\w+)/(?P<nid>\d+).html$',views.article),
    url(r'^cal_read_counts.html$',views.cal_read_counts),
    url(r'^(?P<site>\w+)/(?P<key>((tag)|(date)|(category)))/(?P<val>\w+-*\w*)/', views.filter),
    url(r'^(\w+)',views.home),
    url(r'^',views.index),
]
