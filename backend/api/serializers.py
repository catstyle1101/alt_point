from rest_framework import serializers as s

from clients import models as m


class JobSerializer(s.ModelSerializer):

    class Meta:
        model = m.Job
        fields = '__all__'


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


class ClientSerializer(s.ModelSerializer):
    jobs = JobSerializer(many=True)
    passport = PassportSerializer()
    livingAddress = AddressSerializer()
    regAddress = AddressSerializer()
    communications = CommunicationsSerializer(many=True)
    children = ChildrenSerializer(many=True)

    class Meta:
        model = m.Client
        fields = '__all__'
