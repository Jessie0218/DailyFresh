# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('Goods', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('User', '0001_initial'),
        ('Orders', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderinfo',
            name='addr',
            field=models.ForeignKey(verbose_name='地址', to='User.Address'),
        ),
        migrations.AddField(
            model_name='orderinfo',
            name='user',
            field=models.ForeignKey(verbose_name='用户', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='ordergoods',
            name='order',
            field=models.ForeignKey(verbose_name='订单', to='Orders.OrderInfo'),
        ),
        migrations.AddField(
            model_name='ordergoods',
            name='sku',
            field=models.ForeignKey(verbose_name='商品SKU', to='Goods.GoodsSKU'),
        ),
    ]
