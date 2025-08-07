import logging
import traceback
import json

from rest_framework.response import Response
from rest_framework import status

logger = logging.getLogger("django.request")

def log_internal_error(request, e):
  correlation_id = getattr(request, "correlation_id", "unknown")
  log_data = {
    "error": str(e),
    "type": type(e).__name__,
    "traceback": traceback.format_exc(),
    "path": request.path,
    "method": request.method,
    "correlation_id": correlation_id,
  }

  logger.error(json.dumps(log_data))

  return

def return_internal_error_response():
  return Response({
    "error": "Internal Server Error",
  }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)