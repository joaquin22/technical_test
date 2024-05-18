# Generated by Django 4.2 on 2024-05-17 17:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("loan", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="loan",
            name="contract_version",
            field=models.CharField(
                blank=True,
                default="",
                max_length=30,
                null=True,
                verbose_name="Contract Version",
            ),
        ),
    ]
