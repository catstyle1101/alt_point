from drf_yasg import openapi as o

from clients import models as m


def make_description(model, field, attr):
    field_name = getattr(model, field).field.verbose_name
    result = f"{field_name}\n"
    types = getattr(model, attr)
    for link, name in types:
        result += f"* {link} - {name}\n"
    return result


child = o.Schema(
    title='Children',
    type=o.TYPE_OBJECT,
    properties={
        'id': o.Schema(
            type=o.TYPE_STRING, format=o.FORMAT_UUID, read_only=True
        ),
        'name': o.Schema(title=m.Child.name.field.verbose_name, type=o.TYPE_STRING, example='Иван', nullable=m.Child.name.field.blank),
        'surname': o.Schema(title=m.Child.surname.field.verbose_name, type=o.TYPE_STRING, example='Иванов', nullable=m.Child.surname.field.blank),
        'patronymic': o.Schema(title=m.Child.patronymic.field.verbose_name, type=o.TYPE_STRING, example='Иванович', nullable=m.Child.patronymic.field.blank),
        'dob': o.Schema(title=m.Child.dob.field.verbose_name,
            type=o.FORMAT_DATETIME, example='2022-07-10T00:00:00.000Z', nullable=m.Child.dob.field.blank
        ),
    },
)

document_id = o.Schema(
    title='Document id',
    type=o.TYPE_OBJECT,
    properties={
        'id': o.Schema(
            type=o.TYPE_STRING, format=o.FORMAT_UUID, read_only=True
        ),
    },
)

passport = o.Schema(
    title='Passport',
    type=o.TYPE_OBJECT,
    properties={
        'id': o.Schema(
            type=o.TYPE_STRING, format=o.FORMAT_UUID, read_only=True
        ),
        'series': o.Schema(
            title=m.Passport.series.field.verbose_name,
            type=o.TYPE_STRING,
            example='7474',
            nullable=m.Passport.series.field.blank,
        ),
        'number': o.Schema(
            title=m.Passport.number.field.verbose_name,
            type=o.TYPE_STRING,
            example='123456',
            nullable=m.Passport.number.field.blank,
        ),
        'giver': o.Schema(
            title=m.Passport.giver.field.verbose_name,
            type=o.TYPE_STRING,
            example='ОУФМ Челябинской обл. по Центральному р-ну гор.Челябинска',
            nullable=m.Passport.giver.field.blank,
        ),
        'dateIssued': o.Schema(
            title=m.Passport.dateIssued.field.verbose_name,
            type=o.FORMAT_DATETIME,
            example='2022-07-10T00:00:00.000Z',
            nullable=m.Passport.dateIssued.field.blank,
        ),
    },
)
communication = o.Schema(
    title=m.Communication._meta.verbose_name,
    type=o.TYPE_OBJECT,
    properties={
        'id': o.Schema(
            type=o.TYPE_STRING, format=o.FORMAT_UUID, read_only=True
        ),
        'type': o.Schema(
            title=m.Communication.type.field.verbose_name,
            type=o.TYPE_STRING,
            enum=[i[0] for i in m.Communication.COMMUNICATION_TYPE],
            description=make_description(m.Communication, 'type', 'COMMUNICATION_TYPE'),
            nullable=m.Communication.type.field.blank,
        ),
        'value': o.Schema(
            title=m.Communication.value.field.verbose_name,
            type=o.TYPE_STRING,
            example='89992223322',
            nullable=m.Communication.value.field.blank,
        )
    }
)

address = o.Schema(
    title='Адрес',
    type=o.TYPE_OBJECT,
    properties={
        'id': o.Schema(
            type=o.TYPE_STRING, format=o.FORMAT_UUID, read_only=True
        ),
        'zipCode': o.Schema(
            title=m.Address.zipCode.field.verbose_name,
            type=o.TYPE_STRING,
            example='444005',
            nullable=m.Address.zipCode.field.blank,
        ),
        'country': o.Schema(
            title=m.Address.country.field.verbose_name,
            type=o.TYPE_STRING,
            example='Россия',
            nullable=m.Address.country.field.blank,
        ),
        'region': o.Schema(
            title=m.Address.region.field.verbose_name,
            type=o.TYPE_STRING,
            example='Саратовская область',
            nullable=m.Address.region.field.blank,
        ),
        'city': o.Schema(
            title=m.Address.city.field.verbose_name,
            type=o.TYPE_STRING,
            example='Саратов',
            nullable=m.Address.city.field.blank,
        ),
        'street': o.Schema(
            title=m.Address.street.field.verbose_name,
            type=o.TYPE_STRING,
            example='ул. Пушкина',
            nullable=m.Address.street.field.blank,
        ),
        'house': o.Schema(
            title=m.Address.house.field.verbose_name,
            type=o.TYPE_STRING,
            example='12а',
            nullable=m.Address.house.field.blank,
        ),
        'apartment': o.Schema(
            title=m.Address.apartment.field.verbose_name,
            type=o.TYPE_STRING,
            example='101а',
            nullable=m.Address.apartment.field.blank,
        ),
    },
)

job = o.Schema(
    title='Job',
    type=o.TYPE_OBJECT,
    properties={
        'id': o.Schema(
            type=o.TYPE_STRING, format=o.FORMAT_UUID, read_only=True
        ),
        'type': o.Schema(
            title=m.Job.type.field.verbose_name,
            type=o.TYPE_STRING,
            enum=[i[0] for i in m.Job.TYPES],
            description=make_description(m.Job, 'type', 'TYPES'),
            nullable=m.Job.type.field.blank,
        ),
        'dateEmp': o.Schema(
            title=m.Job.dateEmp.field.verbose_name,
            type=o.TYPE_STRING,
            format=o.FORMAT_DATETIME,
            example='2022-07-10T00:00:00.000Z',
            nullable=m.Job.dateEmp.field.blank,
        ),
        'dateDismissal': o.Schema(
            title=m.Job.dateDismissal.field.verbose_name,
            type=o.TYPE_STRING,
            format=o.FORMAT_DATETIME,
            example='2022-07-10T00:00:00.000Z',
            nullable=m.Job.dateDismissal.field.blank,
        ),
        'monIncome': o.Schema(
            title=m.Job.monIncome.field.verbose_name,
            type=o.FORMAT_DECIMAL,
            example=55.55,
            nullable=m.Job.monIncome.field.blank,
        ),
        'tin': o.Schema(
            title=m.Job.tin.field.verbose_name,
            type=o.TYPE_STRING,
            example='402912408810',
            nullable=m.Job.tin.field.blank,
        ),
        'factAddress': o.Schema(
            title=m.Job.factAddress.field.verbose_name,
            type=o.TYPE_OBJECT,
            properties=address.properties,
            nullable=m.Job.factAddress.field.blank,
        ),
        'jurAddress': o.Schema(
            title=m.Job.jurAddress.field.verbose_name,
            type=o.TYPE_OBJECT,
            properties=address.properties,
            nullable=m.Job.jurAddress.field.blank,
        ),
        'phoneNumber': o.Schema(
            title=m.Job.phoneNumber.field.verbose_name,
            type=o.TYPE_STRING,
            example='89221113322',
            nullable=m.Job.phoneNumber.field.blank,
        ),
    },
)

user_schema = o.Schema(
    title='Create client',
    type=o.TYPE_OBJECT,
    properties={
        'id': o.Schema(
            type=o.TYPE_STRING, format=o.FORMAT_UUID, read_only=True
        ),
        'name': o.Schema(type=o.TYPE_STRING, example='Иван'),
        'surname': o.Schema(type=o.TYPE_STRING, example='Иванов'),
        'patronymic': o.Schema(type=o.TYPE_STRING, example='Иванович'),
        'dob': o.Schema(
            type=o.TYPE_STRING,
            format=o.FORMAT_DATETIME,
            example='2022-07-10T00:00:00.000Z',
        ),
        'children': o.Schema(type=o.TYPE_ARRAY, items=child, default=[]),
        'documentIds': o.Schema(
            type=o.TYPE_ARRAY, items=document_id, default=[]
        ),
        'passport': o.Schema(
            type=o.TYPE_OBJECT, properties=passport.properties
        ),
        'livingAddress': o.Schema(
            type=o.TYPE_OBJECT, properties=address.properties
        ),
        'regAddress': o.Schema(
            type=o.TYPE_OBJECT, properties=address.properties
        ),
        'jobs': o.Schema(type=o.TYPE_ARRAY, items=job, default=[]),
        'typeEducation': o.Schema(
            title=m.Client.typeEducation.field.verbose_name,
            type=o.TYPE_STRING,
            enum=[i[0] for i in m.Client.EDUCATION_TYPES],
            description=make_description(m.Client, 'typeEducation', 'EDUCATION_TYPES'),
            nullable=m.Client.typeEducation.field.blank,
        ),
        'monIncome': o.Schema(
            title=m.Client.monIncome.field.verbose_name,
            type=o.TYPE_NUMBER,
            format=o.FORMAT_DECIMAL,
            example=55.55,
            nullable=m.Client.monIncome.field.blank,
        ),
        'monExpenses': o.Schema(
            title=m.Client.monExpenses.field.verbose_name,
            type=o.TYPE_NUMBER,
            format=o.FORMAT_DECIMAL,
            example=55.55,
            nullable=m.Client.monExpenses.field.blank,
        ),
        'communications': o.Schema(
            type=o.TYPE_ARRAY,
            items=communication,
            default=[],
        )
    },
)
