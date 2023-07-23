from django.http import JsonResponse
from rest_framework import status


class DRF500Middleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if response.status_code == 500:
            return JsonResponse(
                {
                    'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "code": "INTERNAL_SERVER_ERROR"
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return response
