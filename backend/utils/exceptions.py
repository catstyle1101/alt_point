from rest_framework import status
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        if response.status_code == status.HTTP_400_BAD_REQUEST:
            response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
            response.data = {
                'status': status.HTTP_422_UNPROCESSABLE_ENTITY,
                'code': 'VALIDATION_EXCEPTION',
                'errors': response.data
            }
    return response
