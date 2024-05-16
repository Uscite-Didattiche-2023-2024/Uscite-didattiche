from django.utils.deprecation import MiddlewareMixin
from .models import Notifica

class AddNotificationContextMiddleware(MiddlewareMixin):
    def process_template_response(self, request, response):
        if hasattr(response, 'context_data'):
            response.context_data['notifiche'] = Notifica.objects.all()
        return response
