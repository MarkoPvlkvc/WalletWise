# Generated by Django 4.2.6 on 2024-01-24 18:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_income_delete_userprofile'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ExpenseCategory',
            new_name='Category',
        ),
    ]
