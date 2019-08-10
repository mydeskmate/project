# Generated by Django 2.2.4 on 2019-08-10 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='article_type_id',
            field=models.IntegerField(choices=[(1, 'Python'), (2, 'Linux'), (3, '容器'), (4, '数据库')], default=None),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='avatar',
            field=models.ImageField(upload_to='static/images', verbose_name='头像'),
        ),
    ]
