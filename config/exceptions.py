import logging

from rest_framework.views import exception_handler

logger = logging.getLogger("api")


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is None:
        return None

    request = context.get("request")
    status_code = response.status_code

    if request:
        logger.warning(
            "Erro de API: %s %s -> %s",
            request.method,
            request.path,
            status_code,
        )

    if isinstance(response.data, dict):
        response.data["status_code"] = status_code
    else:
        response.data = {
            "detail": response.data,
            "status_code": status_code,
        }

    return response