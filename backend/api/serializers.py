from django.db import transaction
from rest_framework import serializers as s
from rest_framework.utils import model_meta

from clients import models as m


class PassportSerializer(s.ModelSerializer):

    class Meta:
        model = m.Passport
        fields = '__all__'

    def validate(self, attrs):
        if m.Passport.objects.filter(
            series=attrs.get('series'), number=attrs.get('number')
        ).exists():
            raise s.ValidationError(
                'Паспорт с такой серией и номером уже существует'
            )
        return attrs


class DocumentsSerializer(s.ModelSerializer):
    class Meta:
        model = m.Document
        fields = '__all__'


class AddressSerializer(s.ModelSerializer):
    class Meta:
        model = m.Address
        fields = '__all__'


class CommunicationsSerializer(s.ModelSerializer):
    class Meta:
        model = m.Communication
        fields = '__all__'


class ChildrenSerializer(s.ModelSerializer):
    class Meta:
        model = m.Child
        fields = '__all__'


class JobSerializer(s.ModelSerializer):
    factAddress = AddressSerializer()
    jurAddress = AddressSerializer()

    class Meta:
        model = m.Job
        fields = '__all__'


class BaseClientSerializer(s.ModelSerializer):
    jobs = JobSerializer(many=True)
    communications = CommunicationsSerializer(many=True)
    children = ChildrenSerializer(many=True)
    passport = PassportSerializer()
    livingAddress = AddressSerializer()
    regAddress = AddressSerializer()
    documentIds = DocumentsSerializer(many=True)

    class Meta:
        abstract = True

    def _add_fk_related_object(self, validated_data, key, model):
        if validated_data is None:
            validated_data[key] = None
        elif value := validated_data.pop(key):
            validated_data[key] = model.objects.create(**value)

    def _add_m2m_related_object(
        self, data, validated_data, key, model, parent
    ):
        if data is None:
            validated_data[key] = None
        all_instances = list()
        for item in data:
            if pk := item.get('id'):
                try:
                    instance = model.objects.get(pk=pk)
                except Exception:
                    continue
                for k, v in item.items():
                    setattr(instance, k, v)
                    all_instances.append(instance)
            else:
                all_instances.append(model.objects.create(**item))
        validated_data[key] = all_instances
        attr = getattr(parent, key)
        attr.set(all_instances)

    def create(self, validated_data):
        with transaction.atomic():
            if 'spouse' in validated_data:
                serializer = SpouseClientSerializer(
                    data=validated_data.pop('spouse')
                )
                if serializer.is_valid(raise_exception=True):
                    obj = serializer.save()
                    validated_data['spouse'] = obj
        for key, model in (
            ('passport', m.Passport),
            ('livingAddress', m.Address),
            ('regAddress', m.Address),
        ):
            self._add_fk_related_object(validated_data, key, model)

        jobs = validated_data.pop('jobs')
        communications = validated_data.pop('communications')
        childrens = validated_data.pop('children')
        documents = validated_data.pop('documentIds')
        client = m.Client.objects.create(**validated_data)
        for key, data, model in (
            ('jobs', jobs, m.Job),
            ('communications', communications, m.Communication),
            ('children', childrens, m.Child),
            ('documentIds', documents, m.Document),
        ):
            self._add_m2m_related_object(
                data, validated_data, key, model, client
            )
        if 'spouse' in validated_data:
            spouse = validated_data['spouse']
            spouse.spouse_id = client.pk
            if (
                client.passport.series == spouse.passport.series
                and client.passport.number == spouse.passport.number
            ):
                raise s.ValidationError('Серия и номер паспортов одинаковые')
            spouse.save()
        return client

    def _update_instance(self, validated_data, key, model):
        if key in validated_data:
            nested_serializer = self.fields[key]
            nested_instance = getattr(model, key)
            nested_data = validated_data.pop(key)
            if nested_data is None:
                setattr(model, key, None)
            else:
                nested_serializer.update(nested_instance, nested_data)

    def update(self, client, validated_data):
        if 'spouse' in validated_data:
            data = validated_data.pop('spouse')
            if data is None:
                client.spouse = data
            else:
                serializer = SpouseClientSerializer(data=data)
                if serializer.is_valid(raise_exception=True):
                    obj = serializer.save()
                    validated_data['spouse'] = obj
        rel_fields = {
            'jobs': m.Job,
            'communications': m.Communication,
            'children': m.Child,
            'passport': m.Passport,
            'livingAddress': m.Address,
            'regAddress': m.Address,
            'documentIds': m.Address,
            'spouse': m.Client,
        }
        fields = [i for i in validated_data]
        for field in fields:
            model = rel_fields.get(field)
            f = validated_data.get(field)
            if isinstance(f, dict):
                if pk := self.initial_data.get(field).get('id'):
                    try:
                        instance = model.objects.get(pk=pk)
                    except Exception as e:
                        raise s.ValidationError(
                            f'field {field} with {pk} does not exist.'
                        )
                    serializer = self.fields[field]
                    data = validated_data.pop(field)
                    if data is None:
                        setattr(client, field, None)
                    else:
                        serializer.update(instance, data)
                        validated_data[field] = serializer
                else:
                    self._add_fk_related_object(validated_data, field, model)
            elif isinstance(f, list):
                self._add_m2m_related_object(
                    validated_data.pop(field),
                    validated_data,
                    field,
                    model,
                    client,
                )

        info = model_meta.get_field_info(client)
        m2m_fields = []
        for attr, value in validated_data.items():
            if attr in info.relations and info.relations[attr].to_many:
                m2m_fields.append((attr, value))
            else:
                setattr(client, attr, value)
        client.save()
        for attr, value in m2m_fields:
            field = getattr(client, attr)
            field.set(value)

        return client


class SpouseClientSerializer(BaseClientSerializer):
    class Meta:
        model = m.Client
        exclude = ('spouse',)


class ClientSerializer(BaseClientSerializer):
    spouse = SpouseClientSerializer()

    class Meta:
        model = m.Client
        fields = '__all__'
