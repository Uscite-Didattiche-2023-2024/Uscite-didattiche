from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import render
from .models import Notifica


class AddNotificationContextMiddleware(MiddlewareMixin):
    def process_template_response(self, request, response):
        if hasattr(response, "context_data"):
            response.context_data["notifiche"] = Notifica.objects.all()
        return response


class Custom403Middleware(MiddlewareMixin):
    def process_response(self, request, response):
        if response.status_code == 403:
            return render(request, "gite/403.html")
        return response
