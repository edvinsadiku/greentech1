# Generated by Django 5.0.6 on 2024-06-10 23:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('GT', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='service',
            old_name='name',
            new_name='title',
        ),
    ]
