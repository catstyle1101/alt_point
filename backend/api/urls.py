from django.urls import include, path
from rest_framework.routers import SimpleRouter

from api.views import ClientViewset

app_name = 'api'

router = SimpleRouter()

router.register('clients', ClientViewset, basename='clients')

urlpatterns = [
    path('', include(router.urls)),
]
