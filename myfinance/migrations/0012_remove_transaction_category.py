# Generated by Django 4.2 on 2025-03-06 04:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myfinance', '0011_alter_category_cat_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='category',
        ),
    ]
