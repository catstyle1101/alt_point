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


class ClientSerializer(s.ModelSerializer):
    jobs = JobSerializer(many=True, read_only=True)
    communications = CommunicationsSerializer(many=True, read_only=True)
    children = ChildrenSerializer(many=True, read_only=True)

    class Meta:
        model = m.Client
        fields = '__all__'
