# Generated by Django 4.2.3 on 2023-07-21 04:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0017_alter_passport_unique_together'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='passport',
            unique_together=set(),
        ),
    ]
