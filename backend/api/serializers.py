from django.conf import settings
from rest_framework import serializers as s

from clients import models as m


class PassportSerializer(s.ModelSerializer):

    class Meta:
        model = m.Passport
        fields = '__all__'


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

class SpouseClientSerializer(s.ModelSerializer):
    jobs = JobSerializer(many=True)
    communications = CommunicationsSerializer(many=True)
    children = ChildrenSerializer(many=True)
    passport = PassportSerializer()
    livingAddress = AddressSerializer()
    regAddress = AddressSerializer()
    documentIds = DocumentsSerializer(many=True)

    class Meta:
        model = m.Client
        exclude = ('spouse',)


class ClientSerializer(s.ModelSerializer):
    jobs = JobSerializer(many=True)
    communications = CommunicationsSerializer(many=True)
    children = ChildrenSerializer(many=True)
    passport = PassportSerializer()
    livingAddress = AddressSerializer()
    regAddress = AddressSerializer()
    documentIds = DocumentsSerializer(many=True)
    # spouse = SpouseClientSerializer()

    class Meta:
        model = m.Client
        fields = '__all__'

    def _add_fk_related_object(
            self, validated_data, key, model):
        if value := validated_data.pop(key):
            validated_data[key] = model.objects.create(**value)

    def _add_m2m_related_object(self, data, validated_data, key, model, parent):
        if data is None:
            return
        all_instances = [model.objects.create(**i) for i in data]
        validated_data[key] = all_instances
        attr = getattr(parent, key)
        attr.set(all_instances)

    def create(self, validated_data):
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
                data, validated_data, key, model, client)
        return client

    d
