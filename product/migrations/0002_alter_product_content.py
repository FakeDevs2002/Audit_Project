# Generated by Django 5.0.3 on 2024-03-09 16:28

import django_ckeditor_5.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='content',
            field=django_ckeditor_5.fields.CKEditor5Field(verbose_name='content'),
        ),
    ]