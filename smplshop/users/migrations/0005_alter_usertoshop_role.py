# Generated by Django 4.0.8 on 2022-12-30 02:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_user_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usertoshop',
            name='role',
            field=models.CharField(choices=[('owner', 'Store Owner'), ('manager', 'Store Manager'), ('shipper', 'Store Delivery'), ('buyer', 'Store Buyer')], default='buyer', max_length=20, verbose_name='Role'),
        ),
    ]
