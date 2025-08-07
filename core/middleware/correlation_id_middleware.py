import uuid

class CorrelationIdMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path
        
        if not path.startswith("/api"):
            return self.get_response(request)
          
        correlation_id = request.META.get("HTTP_X_CORRELATION_ID") or str(uuid.uuid4())
        request.correlation_id = correlation_id

        response = self.get_response(request)

        if hasattr(request, "correlation_id"):
            response["X-Correlation-ID"] = request.correlation_id

        return response