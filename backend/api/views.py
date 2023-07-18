from rest_framework.viewsets import ModelViewSet

from api import serializers as s
from api.pagination import ProjectViewPagination
from clients import models as m



class ClientViewset(ModelViewSet):
    queryset = m.Client.objects.all()
    serializer_class = s.ClientSerializer
    pagination_class = ProjectViewPagination
