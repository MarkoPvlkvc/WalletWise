# Generated by Django 4.2.6 on 2024-02-03 19:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0007_alter_expense_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='description',
            field=models.CharField(max_length=30),
        ),
    ]
