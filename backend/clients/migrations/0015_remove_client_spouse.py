# Generated by Django 4.2.3 on 2023-07-20 11:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0014_client_spouse'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='client',
            name='spouse',
        ),
    ]