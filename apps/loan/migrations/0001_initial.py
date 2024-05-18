# Generated by Django 4.2 on 2024-05-16 00:25

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("customer", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Loan",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(default=datetime.datetime.now)),
                ("updated_at", models.DateTimeField(default=datetime.datetime.now)),
                (
                    "external_id",
                    models.CharField(max_length=60, verbose_name="External ID"),
                ),
                ("amount", models.FloatField(verbose_name="Amount")),
                ("outstanding", models.FloatField(verbose_name="Outstanding")),
                (
                    "contract_version",
                    models.CharField(max_length=30, verbose_name="Contract Version"),
                ),
                (
                    "status",
                    models.PositiveSmallIntegerField(
                        choices=[
                            (1, "Pending"),
                            (2, "Active"),
                            (3, "Rejected"),
                            (4, "Paid"),
                        ],
                        default=1,
                        verbose_name="Status",
                    ),
                ),
                ("taken_at", models.DateTimeField(blank=True, null=True)),
                (
                    "customer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="customer.customer",
                    ),
                ),
            ],
            options={
                "verbose_name": "Loan",
                "verbose_name_plural": "Loans",
            },
        ),
    ]
