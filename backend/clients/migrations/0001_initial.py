# Generated by Django 4.2.3 on 2023-07-18 09:03

import clients.validators
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('createdAt', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updatedAt', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('zipCode', models.CharField(max_length=6, verbose_name='Почтовый индекс')),
                ('country', models.CharField(max_length=200, verbose_name='Страна')),
                ('region', models.CharField(max_length=200, verbose_name='Регион, область')),
                ('city', models.CharField(max_length=200, verbose_name='Город')),
                ('street', models.CharField(max_length=200, verbose_name='Улица')),
                ('house', models.CharField(max_length=20, verbose_name='Номер дома')),
                ('apartment', models.CharField(blank=True, max_length=20, verbose_name='Номер квартиры, офиса и т.д.')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Child',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('createdAt', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updatedAt', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('name', models.CharField(max_length=100, verbose_name='Имя')),
                ('surname', models.CharField(max_length=100, verbose_name='Фамилия')),
                ('patronymic', models.CharField(max_length=100, verbose_name='Отчество')),
                ('dob', models.DateField(verbose_name='День рождения')),
            ],
            options={
                'verbose_name': 'Ребенок клиента',
                'verbose_name_plural': 'Дети клиента',
            },
        ),
        migrations.CreateModel(
            name='Communication',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('type', models.CharField(choices=[('email', 'email'), ('phone', 'phone')], max_length=5, verbose_name='Тип')),
                ('value', models.CharField(max_length=50, verbose_name='Значение средства связи')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Passport',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('createdAt', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updatedAt', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('series', models.CharField(max_length=4, validators=[clients.validators.passport_series_validator], verbose_name='Серия')),
                ('number', models.CharField(max_length=6, validators=[clients.validators.passport_number_validator], verbose_name='Номер')),
                ('giver', models.CharField(max_length=200, verbose_name='Кем выдан')),
                ('dateIssued', models.DateField(verbose_name='Дата выдачи')),
            ],
            options={
                'verbose_name': 'Паспорт',
                'verbose_name_plural': 'Паспорта',
            },
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('createdAt', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updatedAt', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('type', models.CharField(blank=True, choices=[('Основная работа', 'Основная работа'), ('Частичная занятость', 'Частичная занятость')], max_length=20, verbose_name='Тип работы')),
                ('dateEmp', models.DateField(blank=True, verbose_name='Дата трудоустройства')),
                ('dateDismissal', models.DateField(blank=True, verbose_name='Дата увольнения')),
                ('monIncome', models.DecimalField(blank=True, decimal_places=2, max_digits=10, verbose_name='Доход в месяц')),
                ('tin', models.CharField(blank=True, max_length=12, validators=[clients.validators.tin_validator], verbose_name='ИНН')),
                ('phoneNumber', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, region='RU', verbose_name='Телефон')),
                ('factAddress', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='clients.address', verbose_name='Фактический адрес')),
                ('jurAddress', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='registered_clients', to='clients.address', verbose_name='Юридический адрес')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('createdAt', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updatedAt', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('name', models.CharField(max_length=100, verbose_name='Имя')),
                ('surname', models.CharField(max_length=100, verbose_name='Фамилия')),
                ('patronymic', models.CharField(max_length=100, verbose_name='Отчество')),
                ('dob', models.DateField(verbose_name='День рождения')),
                ('curWorkExp', models.IntegerField(blank=True, verbose_name='На текущем месте работы стаж')),
                ('typeEducation', models.CharField(choices=[('Среднее', 'Среднее'), ('Среднее специальное', 'Среднее специальное'), ('Незаконченное высшее', 'Незаконченное высшее'), ('Высшее', 'Высшее'), ('Два и более высших образований', 'Два и более высших образований'), ('Академическая степень', 'Академическая степень')], max_length=50, verbose_name='Тип образования')),
                ('monIncome', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Суммарный доход в месяц')),
                ('monExpenses', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Суммарный расход в месяц')),
                ('children', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='parent', to='clients.child', verbose_name='Дети')),
                ('communications', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clients.communication')),
                ('documentIds', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clients.document', verbose_name='Идентификаторы документов')),
                ('jobs', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clients.job')),
                ('livingAddress', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='living_person', to='clients.address')),
                ('passport', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='clients.passport')),
                ('regAddress', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='clients.address')),
            ],
            options={
                'verbose_name': 'Клиент',
                'verbose_name_plural': 'Клиенты',
            },
        ),
    ]
