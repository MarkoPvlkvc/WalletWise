# Generated by Django 4.2.6 on 2024-01-26 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_category_icon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='icon',
            field=models.TextField(default='app', max_length=20),
        ),
    ]