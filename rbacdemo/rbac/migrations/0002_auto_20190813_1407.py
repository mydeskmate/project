# Generated by Django 2.2.4 on 2019-08-13 06:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rbac', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=True, related_name='p', to='rbac.Menu', verbose_name='父菜单'),
        ),
        migrations.AlterField(
            model_name='permission',
            name='menu',
            field=models.ForeignKey(blank=True, null=True, on_delete=True, related_name='permissions', to='rbac.Menu', verbose_name='所属菜单'),
        ),
        migrations.AlterField(
            model_name='permission2action2role',
            name='action',
            field=models.ForeignKey(on_delete=True, related_name='permissions', to='rbac.Action', verbose_name='操作'),
        ),
        migrations.AlterField(
            model_name='permission2action2role',
            name='permission',
            field=models.ForeignKey(on_delete=True, related_name='actions', to='rbac.Permission', verbose_name='权限URL'),
        ),
        migrations.AlterField(
            model_name='permission2action2role',
            name='role',
            field=models.ForeignKey(on_delete=True, related_name='p2as', to='rbac.Role', verbose_name='角色'),
        ),
        migrations.AlterField(
            model_name='user2role',
            name='role',
            field=models.ForeignKey(on_delete=True, related_name='users', to='rbac.Role', verbose_name='角色'),
        ),
        migrations.AlterField(
            model_name='user2role',
            name='user',
            field=models.ForeignKey(on_delete=True, related_name='roles', to='rbac.User', verbose_name='用户'),
        ),
    ]
