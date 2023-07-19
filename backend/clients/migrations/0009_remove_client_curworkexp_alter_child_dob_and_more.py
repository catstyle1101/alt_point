# Generated by Django 4.2.3 on 2023-07-19 09:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0008_alter_client_typeeducation_alter_job_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='client',
            name='curWorkExp',
        ),
        migrations.AlterField(
            model_name='child',
            name='dob',
            field=models.DateTimeField(verbose_name='День рождения'),
        ),
        migrations.AlterField(
            model_name='client',
            name='dob',
            field=models.DateTimeField(verbose_name='День рождения'),
        ),
        migrations.AlterField(
            model_name='client',
            name='documentIds',
            field=models.ManyToManyField(blank=True, null=True, related_name='client', to='clients.document', verbose_name='Идентификаторы документов'),
        ),
        migrations.AlterField(
            model_name='job',
            name='dateDismissal',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Дата увольнения'),
        ),
        migrations.AlterField(
            model_name='job',
            name='dateEmp',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Дата трудоустройства'),
        ),
        migrations.AlterField(
            model_name='passport',
            name='dateIssued',
            field=models.DateTimeField(verbose_name='Дата выдачи'),
        ),
    ]
