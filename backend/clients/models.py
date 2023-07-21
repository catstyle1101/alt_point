import uuid

from django.db import models
from django.conf import settings as s
from django.core.exceptions import ValidationError
from phonenumber_field.modelfields import PhoneNumberField

from clients.validators import (
    passport_series_validator,
    passport_number_validator,
    tin_validator,
    zip_code_validator,
)


class BaseIdModel(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)

    class Meta:
        abstract = True


class BaseCreatedAtUpdatedAtModel(BaseIdModel):
    createdAt = models.DateTimeField('Дата создания', auto_now_add=True)
    updatedAt = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        abstract = True


class BasePerson(BaseCreatedAtUpdatedAtModel):
    name = models.CharField(
        'Имя', max_length=s.MAX_NAME_LENGTH, blank=True, null=True
    )
    surname = models.CharField(
        'Фамилия', max_length=s.MAX_NAME_LENGTH, blank=True, null=True
    )
    patronymic = models.CharField(
        'Отчество', max_length=s.MAX_NAME_LENGTH, blank=True, null=True
    )
    dob = models.DateTimeField('День рождения', blank=True, null=True)

    class Meta:
        abstract = True


class Document(BaseIdModel):
    class Meta:
        verbose_name = 'Документ'
        verbose_name_plural = 'Документы'

    def __str__(self):
        return f'Документ номер: {self.id}'


class Address(BaseCreatedAtUpdatedAtModel):
    zipCode = models.CharField(
        'Почтовый индекс',
        max_length=s.ZIP_CODE_LENGTH,
        validators=(zip_code_validator,),
    )
    country = models.CharField('Страна', max_length=s.MAX_COUNTRY_NAME_LENGTH)
    region = models.CharField(
        'Регион, область', max_length=s.MAX_REGION_NAME_LENGTH
    )
    city = models.CharField('Город', max_length=s.MAX_CITY_NAME_LENGTH)
    street = models.CharField('Улица', max_length=s.MAX_STREET_NAME_LENGTH)
    house = models.CharField('Номер дома', max_length=s.MAX_HOUSE_NAME_LENGTH)
    apartment = models.CharField(
        'Номер квартиры, офиса и т.д.',
        max_length=s.MAX_APARTMENT_NAME_LENGTH,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = 'Адрес'
        verbose_name_plural = 'Адреса'

    def __str__(self):
        return f'{self.zipCode}: {self.city}, {self.street}, {self.house}'


class Communication(BaseIdModel):
    email = 'email'
    phone = 'phone'
    COMMUNICATION_TYPE = (
        (email, 'email'),
        (phone, 'phone'),
    )

    type = models.CharField('Тип', choices=COMMUNICATION_TYPE, max_length=5)
    value = models.CharField('Значение средства связи', max_length=50)

    class Meta:
        verbose_name = 'Средство связи'
        verbose_name_plural = 'Средства связи'

    def __str__(self):
        return f'{self.type} -> {self.value}'


class Job(BaseCreatedAtUpdatedAtModel):
    main = 'main'
    part_time = 'part_time'

    TYPES = (
        (main, 'Основная работа'),
        (part_time, 'Частичная занятость'),
    )

    type = models.CharField(
        'Тип работы', max_length=20, choices=TYPES, blank=True
    )
    dateEmp = models.DateTimeField(
        'Дата трудоустройства', blank=True, null=True
    )
    dateDismissal = models.DateTimeField(
        'Дата увольнения', blank=True, null=True
    )
    monIncome = models.DecimalField(
        'Доход в месяц',
        blank=True,
        max_digits=s.MAX_MONEY_DIGITS,
        decimal_places=2,
    )
    tin = models.CharField(
        'ИНН', blank=True, validators=(tin_validator,), max_length=12
    )
    factAddress = models.ForeignKey(
        Address, verbose_name='Фактический адрес', on_delete=models.CASCADE
    )
    jurAddress = models.ForeignKey(
        Address,
        verbose_name='Юридический адрес',
        on_delete=models.CASCADE,
        related_name='registered_clients',
    )
    phoneNumber = PhoneNumberField(
        region='RU',
        verbose_name='Телефон',
        blank=True,
    )  # type: ignore

    class Meta:
        verbose_name = 'Работа'
        verbose_name_plural = 'Работы'

    def __str__(self):
        return f'{self.type}: {self.phoneNumber}, {self.dateEmp}'


class Passport(BaseCreatedAtUpdatedAtModel):
    series = models.CharField(
        'Серия',
        max_length=s.MAX_SERIES_LENGTH,
        blank=False,
        validators=(passport_series_validator,),
    )
    number = models.CharField(
        'Номер',
        max_length=s.MAX_PASSPORT_NUMBER_LENGTH,
        blank=False,
        validators=(passport_number_validator,),
    )
    giver = models.CharField('Кем выдан', max_length=s.MAX_GIVER_LENGTH)
    dateIssued = models.DateTimeField('Дата выдачи')

    class Meta:
        verbose_name = 'Паспорт'
        verbose_name_plural = 'Паспорта'
        unique_together = (('series', 'number'),)

    def __str__(self):
        return (
            f'Паспорт {self.series} {self.number}, Выдан {self.giver}, '
            f'Дата выдачи: {self.dateIssued}'
        )


class Child(BasePerson):
    class Meta:
        verbose_name = 'Ребенок клиента'
        verbose_name_plural = 'Дети клиента'

    def __str__(self):
        return f'{self.name} {self.surname}'


class Client(BasePerson):
    secondary = 'secondary'
    secondarySpecial = 'secondarySpecial'
    incompleteHigher = 'incompleteHigher'
    higher = 'higher'
    twoOrMoreHigher = 'twoOrMoreHigher'
    academicDegree = 'academicDegree'

    EDUCATION_TYPES = (
        (secondary, 'Среднее'),
        (secondarySpecial, 'Среднее специальное'),
        (incompleteHigher, 'Незаконченное высшее'),
        (higher, 'Высшее'),
        (twoOrMoreHigher, 'Два и более высших образований'),
        (academicDegree, 'Академическая степень'),
    )

    children = models.ManyToManyField(
        Child,
        verbose_name='Дети',
        related_name='parent',
        blank=True,
    )
    documentIds = models.ManyToManyField(
        Document,
        verbose_name='Идентификаторы документов',
        related_name='client',
        blank=True,
    )
    passport = models.OneToOneField(
        Passport, on_delete=models.SET_NULL, blank=True, null=True
    )
    livingAddress = models.OneToOneField(
        Address,
        on_delete=models.SET_NULL,
        related_name='living_person',
        blank=True,
        null=True,
    )
    regAddress = models.OneToOneField(
        Address, on_delete=models.SET_NULL, blank=True, null=True
    )
    jobs = models.ManyToManyField(Job, related_name='emploee')
    typeEducation = models.CharField(
        'Тип образования', choices=EDUCATION_TYPES, max_length=50
    )
    monIncome = models.DecimalField(
        'Суммарный доход в месяц',
        max_digits=s.MAX_MONEY_DIGITS,
        decimal_places=s.MAX_MONEY_DECIMAL_PLACES,
    )
    monExpenses = models.DecimalField(
        'Суммарный расход в месяц',
        max_digits=s.MAX_MONEY_DIGITS,
        decimal_places=s.MAX_MONEY_DECIMAL_PLACES,
        blank=True,
        null=True,
    )
    communications = models.ManyToManyField(
        Communication,
        related_name='client',
        blank=True,
    )
    spouse = models.OneToOneField(
        'Client',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='Супруг(а)',
    )

    is_deleted = models.BooleanField(default=False)

    def soft_delete(self):
        self.is_deleted = True
        self.save()

    def restore(self):
        self.is_deleted = False
        self.save()

    def clean(self):
        if self.id == self.spouse_id:
            raise ValidationError("Нельзя подписаться на самого себя")


    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    def __str__(self):
        return f'Клиент: {self.name} {self.surname}'
