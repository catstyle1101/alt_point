from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    # Call the default exception handler first to get the standard error response
    response = exception_handler(exc, context)

    if response is not None:
        # Check if the exception is a validation error
        if response.status_code == 400 and 'detail' in response.data and isinstance(response.data['detail'], list):
            # Customize the validation error response
            response.data = {
                'status': 'error',
                'message': 'Validation failed',
                'errors': response.data['detail']
            }
    return response
