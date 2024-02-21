# Generated by Django 4.2.6 on 2024-02-03 19:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0005_alter_category_icon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='date',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='expense',
            name='tags',
            field=models.ManyToManyField(blank=True, to='myapp.tag'),
        ),
        migrations.AlterField(
            model_name='income',
            name='date',
            field=models.DateTimeField(),
        ),
    ]