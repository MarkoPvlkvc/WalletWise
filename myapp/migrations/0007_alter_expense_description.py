# Generated by Django 4.2.6 on 2024-02-03 19:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_alter_expense_date_alter_expense_tags_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='description',
            field=models.CharField(max_length=20),
        ),
    ]