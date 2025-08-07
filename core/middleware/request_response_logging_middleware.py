import logging
import json
from datetime import datetime

logger = logging.getLogger("django.request")

class RequestResponseLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path
        
        if not path.startswith("/api"):
            return self.get_response(request)
          
        request_time = datetime.now()

        try:
            request_body = request.body.decode('utf-8')
        except:
            request_body = "<non-decodable>"

        response = self.get_response(request)

        response_time = datetime.now()

        log_data = {
            "timestamp": request_time.isoformat(),
            "correlation_id": getattr(request, 'correlation_id', None),
            "method": request.method,
            "path": request.get_full_path(),
            "status_code": response.status_code,
            "remote_addr": request.META.get("REMOTE_ADDR"),
            "content_type": request.META.get("CONTENT_TYPE", ""),
            "accept": request.META.get("HTTP_ACCEPT", ""),
            "request_body": request_body,
            "response_time": (response_time - request_time).total_seconds(),
        }

        try:
            log_data["response_body"] = json.loads(response.content.decode())
        except:
            log_data["response_body"] = "<non-json or too large>"

        logger.info(json.dumps(log_data))

        return response
