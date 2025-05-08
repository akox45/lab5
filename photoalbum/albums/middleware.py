from django.contrib import messages
from django.contrib.auth.models import User

class NotificationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Process notifications before the view
        if request.user.is_authenticated:
            # Get notifications from database
            notifications = request.user.notifications.filter(is_read=False)
            for notification in notifications:
                messages.success(request, notification.message)
                notification.is_read = True
                notification.save()

        response = self.get_response(request)
        return response 