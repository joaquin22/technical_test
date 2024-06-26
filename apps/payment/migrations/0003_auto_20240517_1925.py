# Generated by Django 3.1 on 2024-05-17 19:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0002_rename_paymetdetail_paymentdetail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='external_id',
            field=models.CharField(max_length=60, unique=True, verbose_name='External ID'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='paymentdetail',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
