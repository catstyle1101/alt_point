# Generated by Django 4.2.3 on 2023-07-19 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0009_remove_client_curworkexp_alter_child_dob_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
    ]