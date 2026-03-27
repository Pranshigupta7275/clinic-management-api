from rest_framework.views import exception_handler
from .responses import custom_response

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        message = str(exc.detail) if hasattr(exc, 'detail') else "An error occurred"
        response.data = custom_response(False, None, message)
    
    return response