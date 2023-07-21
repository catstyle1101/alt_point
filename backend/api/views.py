from drf_yasg.utils import swagger_auto_schema
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction

from api import serializers as s
from api import schemas
from api.pagination import ProjectViewPagination
from clients import models as m


class ClientViewset(ModelViewSet):
    queryset = m.Client.objects.filter(is_deleted=False)
    serializer_class = s.ClientSerializer
    pagination_class = ProjectViewPagination
    http_method_names = ['get', 'post', 'head', 'patch', 'delete', 'options']

    @swagger_auto_schema(request_body=schemas.user_schema)
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        """
        Создание клиента.

        ---
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data.get('id'),
            status=status.HTTP_201_CREATED,
            headers=headers,
        )

    def destroy(self, request, *args, **kwargs):
        """
        Мягкое удаление клиента.

        ---
        """
        instance = self.get_object()
        instance.soft_delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def retrieve(self, request, *args, **kwargs):
        """
        Просмотр клиента.

        ---
        """
        return super().retrieve(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        """
        Листинг клиентов.

        ---
        """
        return super().list(request, *args, **kwargs)

    def _change_instance(self, request, key, serializer, instance):
        if key in request.data:
            if request.data[key] is None:
                setattr(instance, key, None)
            else:
                if data := request.data.pop(key):
                    ser = serializer(data=data)
                    if ser.is_valid():
                        ser.save()
                        request.data[key] = ser.data.get('id')

    @swagger_auto_schema(request_body=schemas.user_schema)
    @transaction.atomic
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    # def partial_update(self, request, *args, **kwargs):
    # """
    # Частичное обновление клиента.

    # ---
    # """
    # instance = self.get_object()
    # for key, serializer in (
    #     ('passport', s.PassportSerializer),
    #     ('livingAddress', s.AddressSerializer),
    #     ('regAddress', s.AddressSerializer),

    # ):
    #     self._change_instance(request, key, serializer, instance)
    # partial = kwargs.pop('partial', False)
    # serializer = self.get_serializer(
    #     instance, data=request.data, partial=partial)
    # serializer.is_valid(raise_exception=True)
    # self.perform_update(serializer)

    # if getattr(instance, '_prefetched_objects_cache', None):
    #     instance._prefetched_objects_cache = {}

    # return Response(serializer.data)
