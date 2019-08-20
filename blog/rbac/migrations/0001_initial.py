# Generated by Django 2.2.4 on 2019-08-20 09:02

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Action',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('caption', models.CharField(max_length=32, verbose_name='操作标题')),
                ('code', models.CharField(max_length=32, verbose_name='方法')),
            ],
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('caption', models.CharField(max_length=32, verbose_name='菜单名称')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=True, related_name='p', to='rbac.Menu', verbose_name='父菜单')),
            ],
        ),
        migrations.CreateModel(
            name='Permission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('caption', models.CharField(max_length=32, verbose_name='权限')),
                ('url', models.CharField(max_length=128, verbose_name='URL正则')),
                ('menu', models.ForeignKey(blank=True, null=True, on_delete=True, related_name='permissions', to='rbac.Menu', verbose_name='所属菜单')),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('caption', models.CharField(max_length=32, verbose_name='角色')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=32, verbose_name='用户名')),
                ('password', models.CharField(max_length=64, verbose_name='密码')),
                ('email', models.EmailField(max_length=254, verbose_name='邮箱')),
            ],
        ),
        migrations.CreateModel(
            name='User2Role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.ForeignKey(on_delete=True, related_name='users', to='rbac.Role', verbose_name='角色')),
                ('user', models.ForeignKey(on_delete=True, related_name='roles', to='rbac.User', verbose_name='用户')),
            ],
        ),
        migrations.CreateModel(
            name='Permission2Action2Role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.ForeignKey(on_delete=True, related_name='permissions', to='rbac.Action', verbose_name='操作')),
                ('permission', models.ForeignKey(on_delete=True, related_name='actions', to='rbac.Permission', verbose_name='权限URL')),
                ('role', models.ForeignKey(on_delete=True, related_name='p2as', to='rbac.Role', verbose_name='角色')),
            ],
            options={
                'unique_together': {('permission', 'action', 'role')},
            },
        ),
    ]
