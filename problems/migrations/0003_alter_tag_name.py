# Generated by Django 4.2.5 on 2023-09-05 13:56

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("problems", "0002_alter_problem_number"),
    ]

    operations = [
        migrations.AlterField(
            model_name="tag",
            name="name",
            field=models.CharField(
                max_length=150, unique=True, verbose_name="название"
            ),
        ),
    ]
